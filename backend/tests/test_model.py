import unittest

from apis.model import App


class TestModel(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.invalid_dataset_constant = 'invalid_dataset.csv'
        self.invalid_model_constant = 'invalid_model.mdl'
        self.dataset_path_constant = './backend/tests/test_data/dataset.csv'
        self.model_path_constant = './backend/tests/test_data/model.mdl'

    def test_train_model(self):
        model = (self.app.train_model(dataset=self.dataset_path_constant))
        self.assertIsNotNone(model)

    def test_train_model_svr(self):
        model = (self.app.train_model(dataset=self.dataset_path_constant, model='SVR', test_size=0.2))
        self.assertIsNotNone(model)

    def test_train_model_wrong_kfold(self):
        with self.assertRaises(ValueError):
            self.app.train_model(dataset=self.dataset_path_constant, kfold=0)
        with self.assertRaises(ValueError):
            self.app.train_model(dataset=self.dataset_path_constant, kfold=-1)

    def test_train_model_invalid_data(self):
        with self.assertRaises(FileNotFoundError):
            self.app.train_model(dataset=self.invalid_dataset_constant)

    def test_train_model_invalid_size(self):
        with self.assertRaises(ValueError):
            self.app.train_model(dataset=self.dataset_path_constant, test_size=2.0)
        with self.assertRaises(ValueError):
            self.app.train_model(dataset=self.dataset_path_constant, test_size=-1.0)

    def test_train_model_right_size(self):
        model, _, _ = (self.app.train_model(dataset=self.dataset_path_constant, test_size=0.2))
        self.assertIsNotNone(model)

    def test_predict(self):
        prediction = str(self.app.predict(self.model_path_constant, 'This text was tested by svc'))
        self.assertIsNotNone(prediction)

    def test_predict_invalid_model(self):
        with self.assertRaises(FileNotFoundError):
            self.app.predict(self.invalid_model_constant, 'This text for invalid model')

    def test_predict_empty_text(self):
        with self.assertRaises(ValueError):
            self.app.predict(self.model_path_constant, '')

    def test_visualize(self):
        visualization = (self.app.visualize(self.model_path_constant, 'This text was written for visualization '
                                                                      'prediction'))
        self.assertIsNotNone(visualization)

    def test_visualize_invalid_model(self):
        with self.assertRaises(FileNotFoundError):
            self.app.visualize(self.invalid_model_constant, 'This text for invalid model')

    def test_visualize_empty_text(self):
        with self.assertRaises(ValueError):
            self.app.visualize(self.model_path_constant, '')

    def test_validate(self):
        result = self.app.validate(model=self.model_path_constant, dataset=self.dataset_path_constant,
                                   x='text', y='target', size=0.2)
        self.assertIsNotNone(result)

    def test_validate_invalid_parameters(self):
        with self.assertRaises(FileNotFoundError):
            self.app.validate(model=self.invalid_model_constant, dataset=self.dataset_path_constant, x='text',
                              y='target', size=0.2)
        with self.assertRaises(FileNotFoundError):
            self.app.validate(model=self.model_path_constant, dataset=self.invalid_dataset_constant, x='text',
                              y='target', size=0.2)
        with self.assertRaises(ValueError):
            self.app.validate(model=self.model_path_constant, dataset=self.dataset_path_constant, x='invalid_column',
                              y='invalid_column',
                              size=0.2)
        with self.assertRaises(ValueError):
            self.app.validate(model=self.model_path_constant, dataset=self.dataset_path_constant, x='text', y='target',
                              size=2.0)
        with self.assertRaises(ValueError):
            self.app.validate(model=self.model_path_constant, dataset=self.dataset_path_constant, x='text', y='target',
                              size=-1.0)

    def test_validate_test_size_is_one(self):
        accuracy, f1 = self.app.validate(model=self.model_path_constant, dataset=self.dataset_path_constant,
                                         x='text', y='target', size=1.0)
        self.assertIsNotNone(accuracy)
        self.assertIsNotNone(f1)


if __name__ == '__main__':
    unittest.main()
