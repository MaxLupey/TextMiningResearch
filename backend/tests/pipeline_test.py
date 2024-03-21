import unittest
from classes.customPipeline import CustomPipeline
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer


class TestCustomPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = CustomPipeline()

    def test_create_instance(self):
        self.assertIsInstance(self.pipeline, CustomPipeline)

    def test_get_model(self):
        model = self.pipeline.get_model('SVC')
        self.assertIsInstance(model, SVC)

    def test_get_vectorizer(self):
        vectorizer = self.pipeline.get_vectorizer('TfidfVectorizer')
        self.assertIsInstance(vectorizer, TfidfVectorizer)

    def test_create_pipeline(self):
        pipeline = self.pipeline.create_pipeline('SVC', 'TfidfVectorizer')
        self.assertEqual(len(pipeline.steps), 2)
        self.assertIsInstance(pipeline.steps[0][1], TfidfVectorizer)
        self.assertIsInstance(pipeline.steps[1][1], SVC)

    def test_create_pipeline_invalid_model(self):
        with self.assertRaises(ValueError):
            self.pipeline.create_pipeline('invalid_model', 'TfidfVectorizer')

    def test_create_pipeline_invalid_vectorizer(self):
        with self.assertRaises(ValueError):
            self.pipeline.create_pipeline('SVC', 'invalid_vectorizer')

    def test_create_pipeline_invalid_model_and_vectorizer(self):
        with self.assertRaises(ValueError):
            self.pipeline.create_pipeline('invalid_model', 'invalid_vectorizer')


if __name__ == '__main__':
    unittest.main()
