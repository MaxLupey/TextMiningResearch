from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC, SVR
from sklearn.linear_model import LogisticRegression


class CustomPipeline:
    """
    A utility class to create pipelines with different models and vectorizers.

    Attributes
    ----------
    models : dict
        A dictionary containing different types of models available for use.
    vectorizers : dict
        A dictionary containing various vectorizers for text data processing.

    Methods
    -------
    get_model(name: str)
        Retrieves a specific model based on the provided name.
    get_vectorizer(name: str)
        Retrieves a specific vectorizer based on the provided name.
    create_pipeline(model_name: str, vectorizer_name: str)
        Creates a pipeline by combining a specified model and vectorizer.
    """
    def __init__(self, max_iter=20000, max_features=1000, kernel='linear'):
        """
        Initialize the CustomPipeline class with the provided parameters.

        Parameters
        ----------
        max_iter : int, optional
            Maximum number of iterations to run the model for. Default is 20000.
        max_features : int, optional
            Maximum number of features to use for vectorization. Default is 1000.
        kernel : str, optional
            Kernel to use for the SVC model. Default is 'linear'.
        """
        self.models = {
            'SVC': SVC(kernel=kernel, probability=True, cache_size=200, max_iter=max_iter, verbose=True),
            'SVR': SVR(kernel=kernel, max_iter=max_iter, C=1.0, epsilon=0.2, verbose=True),
            'LogisticRegression': LogisticRegression(max_iter=max_iter, n_jobs=-1, verbose=True)
        }

        self.vectorizers = {
            'CountVectorizer': CountVectorizer(max_df=0.95, min_df=0.01, lowercase=True, max_features=max_features),
            'TfidfVectorizer': TfidfVectorizer(lowercase=True, max_df=0.95, min_df=0.01, stop_words='english'),
            'HashingVectorizer': HashingVectorizer(n_features=max_features)
        }

    def get_model(self, name: str):
        """
        Get the specified model from the available models.

        Parameters
        ----------
        name : str
            Name of the model to retrieve.

        Returns
        -------
        sklearn model
            The requested model object.
        """
        if name not in self.models:
            raise ValueError(f"Model with name '{name}' not found.")
        return self.models[name]

    def get_vectorizer(self, name: str):
        """
        Get the specified vectorizer from the available vectorizers.

        Parameters
        ----------
        name : str
            Name of the vectorizer to retrieve.

        Returns
        -------
        sklearn vectorizer
            The requested vectorizer object.
        """
        if name not in self.vectorizers:
            raise ValueError(f"Vectorizer with name '{name}' not found.")
        return self.vectorizers[name]

    def create_pipeline(self, model_name: str, vectorizer_name: str):
        """
        Create a pipeline combining the specified model and vectorizer.

        Parameters
        ----------
        model_name : str
            Name of the model to use in the pipeline.
        vectorizer_name : str
            Name of the vectorizer to use in the pipeline.

        Returns
        -------
        sklearn Pipeline
            The created pipeline object.
        """
        model = self.get_model(model_name)
        vectorizer = self.get_vectorizer(vectorizer_name)

        return Pipeline([
            ('vectorizer', vectorizer),
            ('model', model)
        ])
