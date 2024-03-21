import base64
import io
import os
import re
from io import StringIO

import joblib
import pandas as pd
from matplotlib import pyplot as plt
from nltk.stem import PorterStemmer
from tqdm import tqdm
from werkzeug.datastructures import FileStorage

from classes.customPipeline import CustomPipeline

tqdm.pandas()


class App:
    """
    The App class provides methods for training a machine learning model, making predictions with the trained model,
    and visualizing the predictions.

    Methods
    -------
    train_model(dataset: str | FileStorage, x: str = 'text', y: str = 'target', kfold: int = 1, test_size: float = 0
                save: bool = True, model: str = 'SVC', vectorizer: str = 'TfidfVectorizer') :
        Trains a machine learning model using the provided dataset and saves it to a file.
    predict(model_path, text) :
        Uses a trained model to make a prediction for a given text input.
    visualize(model_path, text, class_names: str = 'Mostly unreliable, Mostly reliable', num_features=40) :
        Generates an HTML visualization of model predictions for a given text input using LIME (Local Interpretable
        Model-agnostic Explanations).
    validate(dataset, model_path, x, y, size) :
        Validates the accuracy and f1 of a trained model.
    """
    model_not_found_constant = "Model file not found."

    def __init__(self):
        """
        Initialize the App class.
        """
        pass

    @staticmethod
    def train_model(dataset: str | FileStorage, x: str = 'text', y: str = 'target', kfold: int = 1,
                    test_size: float = 0, model: str = 'SVC', vectorizer: str = 'TfidfVectorizer'):
        """
        Trains a machine learning model using the provided dataset and displays accuracy, f1-score.

        Parameters
        ----------
        dataset: str or FileStorage:
            Path to the dataset file or dataset file.
        x : str, optional
            Name of the column containing textual data in the dataset. Default is 'text'.
        y : str, optional
            Name of the column containing target labels in the dataset. Default is 'target'.
        kfold : int, optional
            Number of folds for k-fold cross-validation. Default is 1.
        test_size : float, optional
            Size of the test set. Default is 0.
        model : str, optional
            Name of the machine learning model to use. Default is 'SVC'.
        vectorizer : str, optional
            Name of the vectorizer to use. Default is 'TfidfVectorizer'.

        Returns
        -------
        Pipeline if save is True, else None
            The best model pipeline if save is True, else None.

        Notes
        ------
        This method reads the dataset from the provided path, splits it into training and test sets, and trains a
        machine learning model using k-fold cross-validation. It calculates and prints the accuracy and f1-score for
        each fold. If save is True, it saves and returns the best model pipeline based on f1-score and accuracy.
        """
        validation(test_size, kfold)
        data_x, data_y = read_postprocessing(dataset, x, y)
        pipeline = CustomPipeline().create_pipeline(model, vectorizer)
        if test_size != 0:
            from sklearn.metrics import accuracy_score
            from sklearn.model_selection import ShuffleSplit
            spl = ShuffleSplit(n_splits=kfold, test_size=test_size, random_state=0)
            accuracy_scores = []
            f1_scores = []
            max_f1 = 0.0
            max_accuracy = 0.0
            best_pipeline = None

            for train_index, test_index in tqdm(spl.split(data_x)):
                train_x, test_x = data_x.iloc[train_index], data_x.iloc[test_index]
                train_y, test_y = data_y.iloc[train_index], data_y.iloc[test_index]
                pipeline.fit(train_x, train_y)
                predictions = pipeline.predict(test_x)

                accuracy, f1 = check_model(model, predictions, test_y)

                accuracy_scores.append(accuracy)
                f1_scores.append(f1)
                if f1 > max_f1 and accuracy > max_accuracy:
                    max_f1 = f1
                    max_accuracy = accuracy
                    best_pipeline = pipeline
                print(f"Accuracy: {accuracy}, F1: {f1}")
            return best_pipeline, max_accuracy, max_f1
        else:
            pipeline.fit(data_x, data_y)
            return pipeline, None, None

    @staticmethod
    def predict(model_path: str, text: str):
        """
        Uses a trained model to make a prediction for a given text input.

        Parameters
        ----------
        model_path : str
            Path to the trained model file.
        text : str
            Text input for prediction.

        Returns
        -------
        array
            The predicted class for the input text.

        Raises
        ------
        FileNotFoundError
            If the model file is not found at the specified path.
        ValueError
            If no text is provided for prediction.

        Notes
        ------
        This method loads a pre-trained model from the provided path and uses it to predict the label/classification
        for the given text input. It returns the prediction result.
        """
        if os.path.exists(model_path):
            if not text:
                raise ValueError("No text provided.")
            pipeline = joblib.load(model_path)
            return pipeline.predict([text])
        else:
            raise FileNotFoundError(App.model_not_found_constant)

    @staticmethod
    def visualize(model_path: str, text: str,
                  num_features: int = 40, output_format: str = 'image'):
        """
        Generates an HTML visualization of model predictions for a given text input using LIME (Local Interpretable
        Model-agnostic Explanations).

        Parameters
        ----------
        model_path : str
            Path to the trained model file.
        text : str
            Text input for visualization.
        class_names : str, optional
            List of class names for classification. Default is 'Mostly unreliable, Mostly reliable'.
        num_features : int, optional
            Number of features for the explanation. Default is 40.
        output_format : str, optional
            The output format of the visualization. Default is 'image'.

        Returns
        -------
        str
            The HTML visualization of the model predictions.

        Raises
        ------
        FileNotFoundError
            If the model file is not found at the specified path.
        ValueError
            If no text is provided for visualization.

        Notes
        ------
        This method loads a pre-trained model from the provided path and generates a visualization using LIME to
        explain the model predictions for the given text input. The visualization is returned as an HTML string.
        """
        if os.path.exists(model_path):
            if text == '':
                raise ValueError("No text provided.")
            pipeline = joblib.load(model_path)
            from sklearn.svm import SVR
            if 'model' in pipeline.named_steps and isinstance(pipeline.named_steps['model'], SVR):
                raise ValueError("This model will not be able to visualize the model")

            from lime.lime_text import LimeTextExplainer
            explainer = LimeTextExplainer(class_names=pipeline.classes_)
            exp = explainer.explain_instance(str(text), pipeline.predict_proba, num_features=num_features)
            if output_format == 'image':
                img_buf = io.BytesIO()
                exp.as_pyplot_figure()
                num_y_values = len(exp.as_list())
                height_inches = max(8, int(num_y_values * 0.2))
                plt.gcf().set_size_inches(6, height_inches)  # Set the figure size
                plt.savefig(img_buf, format='png')
                img = base64.b64encode(img_buf.getvalue()).decode()
                return img
            else:
                return exp.as_html()
        else:
            raise FileNotFoundError(App.model_not_found_constant)

    @staticmethod
    def validate(dataset: str | FileStorage, model: str | FileStorage, x: str = 'text', y: str = 'target', size: float = 0.2):
        """
        Validates the accuracy and f1 of a trained model.

        Parameters
        ----------
        dataset : str or FileStorage
            Path to the dataset file or dataset file.
        model : str or FileStorage
            Path to the trained model file or model file.
        x : str, optional
            Name of the column containing textual data in the dataset. Default is 'text'.
        y : str, optional
            Name of the column containing target labels in the dataset. Default is 'target'.
        size : float, optional
            Size of the test set. Default is 0.2.

        Returns
        -------
        tuple
            The accuracy and F1 score of the model.

        Notes
        ------
        This method reads the dataset from the provided path, splits it into training and test sets, and validates the
        accuracy and f1-score of a pre-trained model on the test set. It prints and returns the accuracy and f1-score.
        """
        if isinstance(model, str) and not os.path.exists(model):
            raise FileNotFoundError("Model file not found.")
        elif not model:
            raise ValueError("No model provided.")
        data_x, data_y = read_postprocessing(dataset, x, y)
        from sklearn.model_selection import ShuffleSplit
        if size <= 0.0 or size > 1.0:
            raise ValueError("The test size must be greater than 0.0 and not greater than 1.0.")
        spl = ShuffleSplit(n_splits=1, test_size=size, random_state=0)
        pipeline = joblib.load(model)
        if size != 1:
            for train_index, test_index in spl.split(data_x):
                _, test_x = data_x.iloc[train_index], data_x.iloc[test_index]
                _, test_y = data_y.iloc[train_index], data_y.iloc[test_index]
                predictions = pipeline.predict(test_x)
                accuracy, f1 = check_model(pipeline.named_steps['model'].__class__.__name__, predictions, test_y)
                return accuracy, f1
        else:
            predictions = pipeline.predict(data_x)
            accuracy, f1 = check_model(pipeline.named_steps['model'].__class__.__name__, predictions, data_y)
            return accuracy, f1


def read_postprocessing(dataset: str | FileStorage, x: str, y: str):
    """
    Reads a dataset file and performs preprocessing on the textual data.

    Parameters
    ----------
    dataset : str or FileStorage
        Path to the dataset file or dataset file.
    x : str Name of the column containing textual data in the dataset.
    y : str Name of the column containing target labels in the dataset.

    Returns
    -------
    tuple
        Preprocessed textual data and target labels.

    Raises
    ------
    KeyError
        If the specified columns are not found in the dataset.
    FileNotFoundError
        If the dataset file is not found at the specified path.

    Notes
    ------
    This method reads the dataset from the provided path, preprocesses the textual data by stemming, and returns the
    preprocessed textual data and target labels.
    """
    if isinstance(dataset, str) and not os.path.exists(dataset):
        raise FileNotFoundError("Dataset file not found.")
    if isinstance(dataset, FileStorage):
        dataset = StringIO(dataset.read().decode())
    data = pd.read_csv(filepath_or_buffer=dataset, na_values=[''])
    try:
        data_x = data[x]
        data_y = data[y]
    except KeyError:
        error = ''
        if x not in data.columns:
            error = x
        if y not in data.columns:
            if error != '':
                error += ', '
            error += y
        raise ValueError(f"Column(s) {error} not found in dataset.")
    data_x = data_x.str.lower()
    stemmer = PorterStemmer()
    data_x = data_x.progress_apply(lambda g: ' '.join([stemmer.stem(word) for word in re.sub(
        r'[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]]', '', g).split()]))
    return data_x, data_y


def validation(test_size: float, kfold: int):
    if test_size < 0.0 or test_size >= 1.0:
        raise ValueError("Test size must be at least 0.0 and less than 1.0")
    if kfold < 1:
        raise ValueError("Number of folds must be greater than 0.")


def check_model(model, predictions, test_y):
    from sklearn.metrics import f1_score, accuracy_score
    if model == 'SVR':
        predictions = [round(x) for x in predictions]
    f1 = f1_score(test_y, predictions, average='binary')
    accuracy = accuracy_score(test_y, predictions)
    return accuracy, f1
