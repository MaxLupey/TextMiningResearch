import json
import os
import re
import socket
import time
import uuid
from functools import wraps
from pathlib import Path

import joblib
from google.auth.transport import requests as googl
from configs import configurations
from flask import Flask, jsonify, request, redirect, send_file, url_for, session, make_response
from flask_wtf.csrf import CSRFProtect, generate_csrf
from nltk.stem import PorterStemmer
from google.oauth2 import id_token
from flask_cors import CORS
from apis.model import App
from classes.db_providers.sqlite_provider import SQLiteProvider

data = None
global visualize_option
model_directory = None
model_route_constant = '/model'

def get_flow(secure, address, port):
    return configurations.google_flow(f"{'https://' if secure else 'http://'}{address}:{port}")

def make_pipeline(model_path):
    if check_path(model_path):
        pipeline = joblib.load(model_path)
        from sklearn.svm import SVR
        if 'model' in pipeline.named_steps and isinstance(pipeline.named_steps['model'], SVR):
            print(' ! Attention: This model will not be able to visualize the model, so the /visualize GET '
                  'request will not work')
        return pipeline


def protect(app, app_ref):
    csrf = CSRFProtect(app)
    csrf.init_app(app)
    CORS(app, origins=app_ref, methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"], automatic_options=True,
         supports_credentials=True)
    secrets_path = os.path.join(Path(f"{os.path.abspath('./env')}"), "client_secrets.json")
    app = secret_key(secrets_path, app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    return app


def generate_uuid():
    while True:
        user_id = str(uuid.uuid4())
        if data.get_user_by_uuid(user_id) is None:
            break
    return user_id


def secret_key(secrets_path, app):
    if not os.path.exists(secrets_path):
        print(' * Warning: client_secrets.json not found.')
        exit(1)
    else:
        with open(os.path.join(Path(f"{os.path.abspath('./env')}"), "client_secrets.json")) as f:
            app.secret_key = json.load(f)['web']['client_secret']
            return app


def is_valid_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            if not 0 <= int(part) <= 255:
                raise ValueError("Invalid host")
            return False
    return True


def text_preprocessing():
    """
    Preprocesses the text received from the request.

    Returns
    -------
    str
        The preprocessed text.
    """
    text = request.args.get("text", "").lower()
    if text == "" or text is None:
        raise ValueError("No text provided")
    stemmer = PorterStemmer()
    text = ' '.join(
        [stemmer.stem(word) for word in re.sub(r'[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]]', '', text.lower()).split()])
    return text


def validate_data(host, port):
    """
    Validates the data received from the request.

    Parameters
    ----------
    host : str
        The IP address to run the application on.
    port : int
        The port to run the application on.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the host or port are invalid.
    """
    try:
        if is_valid_ip(host):
            socket.inet_aton(host)
        port = int(port)
        assert 0 <= port <= 65535
    except socket.error:
        raise ValueError("Invalid host")
    except AssertionError:
        raise ValueError("Invalid port")


def create_app(address: str, port: int, model_dir='./tmp', secure=False) -> Flask:
    """
    Runs the Flask application for model prediction and visualization.

    Parameters
    ----------
    secure : bool
        If the connection is secure.
    address : str
        The IP address to run the application on.
    port : int
        The port to run the application on.
    model_dir : str
        The directory to save the models in.

    Returns
    -------
    Flask
        The Flask application.
    """
    model_dir = fix_dir(model_dir)
    print(" * Load model...")
    app_ref = configurations.get_ref()
    validate_data(host=address, port=port)
    print(f" * Running on {address}:{port}")
    global data
    data = SQLiteProvider(db_file='sqlite.db')
    app = Flask(__name__)
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    model = App()
    app = protect(app, app_ref)

    @app.after_request
    def add_headers(response):
        response.headers['Access-Control-Allow-Origin'] = app_ref
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route("/")
    def index():
        return "There is nothing here", 200

    @app.route("/profile_info")
    def profile():
        if auth_check():
            user_id = request.cookies['user_id']
            user_data = data.get_user_by_uuid(user_id)['auth_info']
            response = [user_data['given_name'], user_data['family_name'], user_data['picture']]
            return json.dumps(response), 200
        return "You are not logged in!", 401

    @app.route("/csrf_token")
    def csrf_token():
        return jsonify({"csrf_token": generate_csrf()}), 200

    @app.route("/login")
    def login():
        if auth_check():
            return redirect('/logout')
        flow = get_flow(secure, address, port)
        authorization_url, state = flow.authorization_url()
        session["state"] = state
        return redirect(authorization_url)

    @app.route("/callback")
    def callback():
        global data
        flow = get_flow(secure, address, port)
        flow.fetch_token(authorization_response=request.url)
        if session["state"] != request.args["state"]:
            return "State mismatch", 400
        token = flow.credentials.id_token
        session["google_id_token"] = token
        payload = id_token.verify_oauth2_token(token, googl.Request())
        response = make_response(redirect(app_ref))
        user_data = data.get_user_by_sub(payload['sub'])
        if user_data is None:
            user_id = generate_uuid()
            data.add_user(user_id, token, payload)
        else:
            user_id = user_data['uuid']
            data.update_user(token, payload)
        session["user_id"] = user_id
        response.set_cookie('user_id', user_id, secure=secure, httponly=not secure)
        return response

    @app.route("/logout")
    def logout():
        response = make_response(app_ref)
        response.set_cookie('user_id', '', expires=0, secure=secure, httponly=not secure)
        session.clear()
        return response, 200

    @app.route(f"{model_route_constant}/predict", methods=["GET"])
    @handle_exceptions
    @login_is_required
    def predict():
        """
        Responds to a POST request to predict the class based on the received text.

        Returns
        -------
        JSON
            A JSON object containing the predicted class.

        Raises
        ------
        ValueError
            If params are not valid.
        FileNotFoundError
            If the model is not found.
        Exception
            Error in the backend.
        """
        params = [['model', '', str],
                  ['text', '', str]]
        params = get_params(params)
        model_name = params['model']
        model_path_user = validate_and_set_model_path(model_dir, model_name)
        text = params['text'].lower()
        result = model.predict(model_path_user, text)
        return jsonify({"prediction": str(result), "text": str(text)}), 200

    @app.route(f"{model_route_constant}/visualize", methods=["GET"])
    @handle_exceptions
    @login_is_required
    def visualize():
        """
        Responds to a GET request to visualize the model prediction results.

        Returns
        -------
        HTML
            An HTML string containing the visualization.

        Raises
        ------
        ValueError
            If params are not valid.
        FileNotFoundError
            If the model is not found.
        Exception
            Error in the backend.
        """
        params = [['model', '', str],
                  ['features', 40, int],
                  ['text', '', str],
                  ['output_format', 'image', str]]
        params = get_params(params)
        model_name = params['model']
        model_path_user = validate_and_set_model_path(model_dir, model_name)
        return model.visualize(model_path=model_path_user, text=params['text'].lower(),
                               num_features=params['features'], output_format=params['output_format']), 200

    @app.route(f"{model_route_constant}/train", methods=["POST"])
    @handle_exceptions
    @login_is_required
    def train():
        """
        Responds to a POST request to train the model using uploaded user's dataset.

        Returns
        -------
        String
            A string containing the result of the training process: Accuracy, F1 score and link to download the model.

        Raises
        ------
        ValueError
            If params are not valid.
        FileNotFoundError
            If the model is not found.
        Exception
            Error in the backend.
        """
        print("Dataset is being trained")
        dataset = request.files.get('dataset')
        check_files({'file': dataset, 'name': 'Dataset'})
        params = [['name', '', str],
                  ['x', 'text', str],
                  ['y', 'target', str],
                  ['kfold', 1, int],
                  ['test_size', 0, float],
                  ['model', 'SVC', str],
                  ['vectorizer', 'TfidfVectorizer', str]]
        params = get_params(params)
        print(params)
        model_file, accuracy, f1 = model.train_model(dataset=dataset, x=params['x'], y=params['y'],
                                                     kfold=params['kfold'], test_size=params['test_size'],
                                                     model=params['model'], vectorizer=params['vectorizer'])
        model_file_name = generate_uuid()
        download_link = url_for('download', model_name=model_file_name, _external=True)
        os.makedirs(model_dir, exist_ok=True)
        joblib.dump(model_file, f'{model_dir}/{model_file_name}.mdl')
        global data
        user_id = get_user_id()
        data.add_model(user_id, model_file_name, params['name'], False)
        return jsonify({"accuracy": accuracy, "f1": f1, 'link': download_link}), 200

    @app.route(f"{model_route_constant}/download/<model_name>", methods=["GET"])
    @handle_exceptions
    @login_is_required
    def download(model_name):
        """
        Responds to a GET request to download the model.

        Returns
        -------
        File model
            A file containing the trained model.

        Raises
        ------
        FileNotFoundError
            If the model is not found.
        """
        global model_directory
        model_directory = os.path.join(os.getcwd(), model_dir, f'{model_name}.mdl')

        global data
        user_id = get_user_id()
        model_data = data.get_model_by_uuid(user_id, model_name)
        custom_model_name = check_if_not_none(model_data)

        return send_file(model_directory, as_attachment=True, download_name=f"{custom_model_name}.mdl"), 200

    @app.route(f"{model_route_constant}/validate", methods=["POST"])
    @handle_exceptions
    @login_is_required
    def validate():
        """
        Responds to a POST request to validate the model using uploaded user's dataset.

        Returns
        -------
        String
            A string containing the result of the validation process: Accuracy and F1 score.

        Raises
        ------
        ValueError
            If params are not valid.
        FileNotFoundError
            If the model or dataset is not found.
        Exception
            Error in the backend.

        """
        params = [['model', '', str],
                  ['x', 'text', str],
                  ['y', 'target', str],
                  ['test_size', 0.2, float]]
        params = get_params(params)
        model_name = params['model']
        dataset = request.files.get('dataset')
        check_files({'file': dataset, 'name': 'Dataset'}, {'file': model_name, 'name': 'Model name'})
        model_result = build_tmp_path(model_name, model_dir)

        accuracy, f1 = model.validate(dataset=dataset, model=model_result, x=params['x'], y=params['y'],
                                      size=params['test_size'])
        return jsonify({"accuracy": accuracy, "f1": f1}), 200

    @app.route(f"{model_route_constant}/delete", methods=["DELETE"])
    @handle_exceptions
    @login_is_required
    def model_delete():
        """
        Responds to a POST request to remove the model from the user's models.

        Returns
        -------
        String
            A string containing the result of the removal process.

        Raises
        ------
        ValueError
            If params are not valid.
        FileNotFoundError
            If the model is not found.
        Exception
            Error in the backend.

        """
        params = [['model_uuid', '', str]]
        params = get_params(params)
        model_uuid = params['model_uuid']
        model_path_user = build_tmp_path(model_uuid, model_dir)
        # if not model_path_user or not os.path.exists(model_path_user):
        #     return jsonify({"FileNotFoundError": f"Model {model_uuid} not found"}), 404
        os.remove(model_path_user)
        global data
        data.remove_model(request.cookies['user_id'], model_uuid)
        return jsonify({"result": f"Model {model_uuid} removed"}), 200

    @app.route(f"{model_route_constant}/list", methods=["GET"])
    @handle_exceptions
    @login_is_required
    def get_models():
        """
        Responds to a GET request to get the user's models.

        Returns
        -------
        JSON
            A JSON object containing the user's models.

        Raises
        ------
        ValueError
            If params are not valid.
        FileNotFoundError
            If the model is not found.
        Exception
            Error in the backend.

        """
        global data
        user_id = request.cookies['user_id']
        user_models = data.get_models(user_id, True)
        return jsonify({"models": user_models}), 200

    @app.route(f"{model_route_constant}/list/user", methods=["GET"])
    @handle_exceptions
    @login_is_required
    def get_user_models():
        global data
        user_id = request.cookies['user_id']
        user_models = data.get_models(user_id, False)
        return jsonify({"models": user_models}), 200

    @app.route(f"{model_route_constant}/edit", methods=["PUT"])
    @handle_exceptions
    @login_is_required
    def edit_model():
        """
        Responds to a POST request to rename the user's model.

        Returns
        -------
        JSON
            A JSON object containing the user's models.

        Raises
        ------
        ValueError
            If params are not valid.
        FileNotFoundError
            If the model is not found.
        Exception
            Error in the backend.

        """
        global data
        user_id = request.cookies['user_id']
        params = [['model_uuid', None, str],
                  ['new_model_name', '', str],
                  ['shared', None, str]]
        params = get_params(params)
        print(params)
        model_uuid = params['model_uuid']
        new_model_name = params['new_model_name']
        shared = ts_bool(params['shared'])
        data.edit_model(user_id, model_uuid, new_model_name, shared)

        return jsonify({'result': result_message(model_uuid, new_model_name, shared)}), 200

    @app.route(f"{model_route_constant}/upload", methods=["POST"])
    @handle_exceptions
    @login_is_required
    def upload_model():
        """
        Responds to a POST request to upload the user's model.

        Returns
        -------
        JSON
            A JSON object containing the user's models.

        Raises
        ------
        ValueError
            If params are not valid.
        FileNotFoundError
            If the model is not found.
        Exception
            Error in the backend.

        """
        params = [['model_name', '', str],
                  ['shared', 'false', str]]
        params = get_params(params)
        params['shared'] = ts_bool(params['shared'])
        global data
        user_id = request.cookies['user_id']
        file = request.files.get('file')
        model_name = params['model_name']
        check_files({'file': file, 'name': 'Model'}, {'file': model_name, 'name': 'Model name'})
        try:
            pipeline = joblib.load(file)
        except Exception as e:
            print(e)
            return jsonify({"ValueError": "File is not a model"}), 400
        model_uuid = str(generate_uuid())
        model_path_user = build_tmp_path(model_uuid, model_dir)
        joblib.dump(pipeline, model_path_user)
        data.add_model(user_id, model_uuid, model_name, params['shared'])
        return jsonify({"result": f"Model {model_name} uploaded"}), 200

    return app


def get_params(params: list) -> dict | None:
    """
    Gets the parameters from the request and validates them

    Parameters
    ----------
    params : list
        A list of parameters to get from the request

    Returns
    -------
    dict
        A dictionary of parameters

    Raises
    ------
    ValueError
        If the parameter is not valid
    """
    new_params = {}
    for param in params:
        try:
            param[1] = param[2](request.args.get(param[0], param[1]))
            new_params[param[0]] = param[1]
        except Exception:
            raise ValueError(f'Parameter {param[0]} must be {param[2].__name__}')
    return new_params


def validate_and_set_model_path(model_dir: str, model_name: str = None, ) -> str:
    """
    Checks and sets the model path based on the model name

    Parameters
    ----------
    model_path : str
        Path to the file containing the model to be used.
    model_dir : str
         The directory to save the models in.
    model_name : str, optional
        The model name taken from a query in a URL


    Returns
    -------
    String
        The path to the model that will be used to make a prediction

    Raises
    ------
    ValueError
        Model path or name not provided
    """
    model_path_user = build_tmp_path(model_name, model_dir)
    if not model_path_user:
        raise ValueError('Model name not provided')

    return model_path_user


def build_tmp_path(model_name: str, model_dir: str) -> str:
    """
    Builds the path to the model that was uploaded by the user

    Parameters
    ----------
    model_name : str
        The model name taken from a query in a URL.
    model_dir : str
        The folder path to the model.
    Returns
    -------
    String
        The path to the model that will be used to make a prediction

    """
    if model_name:
        return os.path.join(os.getcwd(), model_dir, f'{model_name}.mdl')


def fix_dir(dir_name):
    return dir_name[:-1] if dir_name[-1] == '/' else dir_name


def check_path(path):
    return path and os.path.exists(path)


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(e)
            return jsonify({"ValueError": str(e)}), 404
        except FileNotFoundError as e:
            print(e)
            return jsonify({"FileNotFoundError": str(e)}), 404
        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            print(e, '\n', error_traceback)
            return jsonify({"BackendError": str(e), "Traceback": error_traceback}), 500

    return wrapper


def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not auth_check():
            return "You are not logged in!", 401
        else:
            return function(*args, **kwargs)

    return wrapper


def is_token_valid(user_id, online=True):
    try:
        global data
        user_data = data.get_user_by_uuid(user_id)
        if online:
            payload = id_token.verify_oauth2_token(user_data['token'], googl.Request())
            expiration_time = payload.get('exp')
        else:
            expiration_time = int(user_data['auth_info']['exp'])
        current_time = int(time.time())
        return expiration_time > current_time
    except ValueError:
        return False


def auth_check():
    global data
    cookies_data = request.cookies
    if 'user_id' not in cookies_data:
        return False
    user_id = cookies_data['user_id']
    if data.get_user_by_uuid(user_id) is None:
        return False

    if not is_token_valid(user_id, False):
        return False
    return True


def generate_uuid():
    return str(uuid.uuid4())


def check_files(*files):
    for file in files:
        if not file['file']:
            raise ValueError(f"{file['name']} not provided")

def result_message(model_uuid, new_model_name, shared):
    result = f'Model {model_uuid} edited: '

    if shared is not None:
        result += f'shared ({shared})'

    if new_model_name:
        result += f'new model name ({new_model_name})'

    return result

def ts_bool(ts_result):
    if is_int(ts_result):
        return bool(ts_result)
    return True if ts_result == 'true' else False

def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def get_user_id():
    return request.cookies['user_id']

def check_if_not_none(file):
    if not file:
        raise ValueError("File not provided")
    return file['name']
