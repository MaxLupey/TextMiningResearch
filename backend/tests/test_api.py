import os
from unittest.mock import patch

import pytest

from apis import api

const_dataset = 'dataset.csv'
const_text = 'Hello World'
const_content_type = 'multipart/form-data'
const_patch = 'apis.model.App'
const_dataset_path = './tests/test_data/dataset.csv'
const_corrupted_dataset_path = './tests/test_data/corrupted_dataset.csv'
const_model_path = './tests/test_data/model.mdl'


def setup_module(module):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(project_root)


def check_models():
    models_in_tmp = None
    if os.path.exists('./tmp'):
        models_in_tmp = [file for file in os.listdir('./tmp') if file.endswith('.mdl')]

    if models_in_tmp:
        model_name = os.path.splitext(models_in_tmp[0])[0]
        return model_name
    return None


@pytest.fixture
def client_svc():
    app = api.create_app('127.0.0.1', 5000, './tmp')
    with app.test_client() as client_svc:
        yield client_svc


def test_validate_data():
    # Test with invalid host
    with pytest.raises(ValueError):
        api.validate_data('256.256.256.256', 5000)

    # Test with invalid port
    with pytest.raises(ValueError):
        api.validate_data('127.0.0.1', 70000)


def test_predict_with_wrong_model_name(client_svc):
    with patch('apis.api.auth_check', return_value=True):
        with patch(const_patch) as mock_app:
            instance = mock_app.return_value
            instance.predict.return_value = 'prediction'
            response = client_svc.get('/model/predict', query_string={'model': 'Wrong model', 'text': const_text})
            assert response.status_code == 404


def test_train_with_fake_dataset(client_svc):
    with patch('apis.api.auth_check', return_value=True):
        with patch(const_patch) as mock_app:
            instance = mock_app.return_value
            instance.train_model.return_value = ('model', 'accuracy', 'f1')

            data = {
                'dataset': (open(const_corrupted_dataset_path, 'rb'), 'corrupted_dataset.csv')
            }

            response = client_svc.post('/model/train', content_type=const_content_type, data=data)
            print(response.get_json())
            assert response.status_code == 400


def test_predict(client_svc):
    with patch('apis.api.auth_check', return_value=True):
        with patch(const_patch) as mock_app:
            instance = mock_app.return_value
            model_name = check_models()
            if model_name:
                instance.predict.return_value = 'prediction'
                response = client_svc.get('/model/predict', query_string={'model': model_name, 'text': const_text})
                print(response.get_json())
                assert response.status_code == 200
                assert response.get_json()['prediction'] in ['[0]', '[1]']

            else:
                print("No models available for testing. Skipping the check.")


def test_visualize(client_svc):
    with patch('apis.api.auth_check', return_value=True):
        with patch(const_patch) as mock_app:
            instance = mock_app.return_value
            model_name = check_models()
            if model_name:
                instance.visualize.return_value = 'visualization'
                response = client_svc.get('/model/visualize', query_string={'model': model_name, 'text': const_text})
                assert response.status_code == 200
            else:
                print("No models available for testing. Skipping the check.")


def mock_add_model(self, uuid, model, _, shared):
    return {'name': uuid, 'uuid': model, 'shared': shared}


def mock_get_user_id():
    return 'test_user_id'


def test_train(client_svc):
    with patch('apis.api.auth_check', return_value=True):
        with patch('classes.db_providers.sqlite_provider.SQLiteProvider.add_model', new=mock_add_model):
            with patch(const_patch) as mock_app:
                with client_svc.application.app_context():
                    with patch('apis.api.get_user_id', new=mock_get_user_id):
                        client_svc.application.config['WTF_CSRF_ENABLED'] = False
                        instance = mock_app.return_value
                        instance.train_model.return_value = ('model', 'accuracy', 'f1')

                        data = {
                            'dataset': (open(const_dataset_path, 'rb'), const_dataset)
                        }

                        response = client_svc.post('/model/train', content_type='multipart/form-data', data=data)
                        print(response.get_data(as_text=True))
                        assert response.status_code == 200
                        assert 'accuracy' in response.get_json()
                        assert 'f1' in response.get_json()
                        assert 'link' in response.get_json()


def test_download(client_svc):
    from classes.db_providers.sqlite_provider import SQLiteProvider
    model_name = SQLiteProvider.get_models(SQLiteProvider(db_file='sqlite.db'), 'test_user_id', use_shared=True)
    if model_name:
        model_name = model_name[0]['uuid']
        with patch('apis.api.auth_check', return_value=True):
            with patch('apis.api.get_user_id', return_value='test_user_id'):
                with patch(const_patch) as mock_app:
                    instance = mock_app.return_value
                    instance.download.return_value = 'file'
                    response = client_svc.get(f'/model/download/{model_name}')
                    assert response.status_code == 200
    else:
        print("No models available for testing. Skipping the check.")


def test_validate(client_svc):
    with patch('apis.api.auth_check', return_value=True):
        with patch(const_patch) as mock_app:
            with client_svc.application.app_context():
                client_svc.application.config['WTF_CSRF_ENABLED'] = False
                instance = mock_app.return_value
                instance.validate.return_value = ('accuracy', 'f1')
                model_name = check_models()
                if model_name:
                    data = {
                        'dataset': open(const_dataset_path, 'rb'),
                    }
                    response = client_svc.post(f'/model/validate?model={model_name}', content_type=const_content_type, data=data)
                    print(response.get_json())
                    assert response.status_code == 200
                    assert 'accuracy' in response.get_json()
                    assert 'f1' in response.get_json()
                else:
                    print("No models available for testing. Skipping the check.")


def test_download_invalid_model(client_svc):
    with patch('apis.api.auth_check', return_value=True):
        with patch('apis.api.get_user_id', return_value='test_user_id'):
            with patch(const_patch) as mock_app:
                instance = mock_app.return_value
                instance.download.return_value = None
                response = client_svc.get('/model/download/wrong_model')
                assert response.status_code == 404


# Validate without dataset
def test_validate_without_dataset(client_svc):
    with patch('apis.api.auth_check', return_value=True):
        with patch(const_patch) as mock_app:
            with client_svc.application.app_context():
                client_svc.application.config['WTF_CSRF_ENABLED'] = False
                model_name = check_models()
                if model_name:
                    instance = mock_app.return_value
                    instance.validate.return_value = ('accuracy', 'f1')
                    data = {
                        'model': (open(const_model_path, 'rb'), model_name)
                    }
                    response = client_svc.post('/model/validate', content_type=const_content_type, data=data)
                    assert response.status_code == 404
                else:
                    print("No models available for testing. Skipping the check.")


# Validate with model name in params: /model/validate?model=model
def test_validate_with_model_name(client_svc):
    with patch('apis.api.auth_check', return_value=True):
        with patch(const_patch) as mock_app:
            with client_svc.application.app_context():
                client_svc.application.config['WTF_CSRF_ENABLED'] = False
                instance = mock_app.return_value
                instance.validate.return_value = ('accuracy', 'f1')
                model_name = check_models()
                if model_name:
                    data = {
                        'dataset': (open(const_dataset_path, 'rb'), const_dataset)
                    }
                    response = client_svc.post(f'/model/validate?model={model_name}', content_type=const_content_type,
                                               data=data)
                    print(response.get_json())
                    assert response.status_code == 200
                    assert 'accuracy' in response.get_json()
                    assert 'f1' in response.get_json()
                else:
                    print("No models available for testing. Skipping the check.")


# Validate with wrong model name in params: /model/validate?model=wrong_model
def test_validate_with_wrong_model_name(client_svc):
    with patch('apis.api.auth_check', return_value=True):
        with patch(const_patch) as mock_app:
            with client_svc.application.app_context():
                client_svc.application.config['WTF_CSRF_ENABLED'] = False
                instance = mock_app.return_value
                instance.validate.return_value = ('accuracy', 'f1')
                data = {
                    'dataset': (open(const_dataset_path, 'rb'), const_dataset)
                }
                response = client_svc.post('/model/validate?model=wrong_model', content_type=const_content_type, data=data)
                assert response.status_code == 404
