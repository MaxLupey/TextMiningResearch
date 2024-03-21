from unittest.mock import patch

import pytest

from apis import api

const_dataset = 'dataset.csv'
const_text = 'Hello World'
const_content_type = 'multipart/form-data'
const_patch = 'apis.model.App'
const_dataset_path = './backend/tests/test_data/dataset.csv'
const_corrupted_dataset_path = './backend/tests/test_data/corrupted_dataset.csv'
const_model_path = './backend/tests/test_data/model.mdl'


@pytest.fixture
def client_svc():
    app = api.create_app('127.0.0.1', 5000, 'model_path', './backend/tests/test_data/')
    with app.test_client() as client_svc:
        yield client_svc


def test_validate_data():
    # Test with invalid host
    with pytest.raises(ValueError):
        api.validate_data('256.256.256.256', 5000, 'model_path')

    # Test with invalid port
    with pytest.raises(ValueError):
        api.validate_data('127.0.0.1', 70000, 'model_path')


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
            instance.predict.return_value = 'prediction'
            response = client_svc.get('/model/predict', query_string={'model': 'model', 'text': const_text})
            assert response.status_code == 200
            assert response.get_json()['prediction'] == '[0]' or '[1]'


def test_visualize(client_svc):
    with patch('apis.api.auth_check', return_value=True):
        with patch(const_patch) as mock_app:
            instance = mock_app.return_value
            instance.visualize.return_value = 'visualization'
            response = client_svc.get('/model/visualize', query_string={'model': 'model', 'text': const_text})
            assert response.status_code == 200


# def test_train(client_svc):
#     with patch('apis.api.auth_check', return_value=True):
#         with patch(const_patch) as mock_app:
#             instance = mock_app.return_value
#             instance.train_model.return_value = ('model', 'accuracy', 'f1')
#
#             data = {
#                 'dataset': (open(const_dataset_path, 'rb'), const_dataset)
#             }
#
#             response = client_svc.post('/model/train', content_type=const_content_type, data=data)
#             print(response.get_json())
#             assert response.status_code == 200
#             assert 'accuracy' in response.get_json()
#             assert 'f1' in response.get_json()
#             assert 'link' in response.get_json()


# def test_download(client_svc):
#     with patch('apis.api.auth_check', return_value=True):
#         with patch(const_patch) as mock_app:
#             instance = mock_app.return_value
#             instance.download.return_value = 'file'
#             response = client_svc.get('/model/download/model')
#             assert response.status_code == 200


def test_validate(client_svc):
    with patch('apis.api.auth_check', return_value=True):
        with patch(const_patch) as mock_app:
            instance = mock_app.return_value
            instance.validate.return_value = ('accuracy', 'f1')
            data = {
                'dataset': (open(const_dataset_path, 'rb'), const_dataset),
                'model': (open(const_model_path, 'rb'), 'model.mdl')
            }
            response = client_svc.post('/model/validate', content_type=const_content_type, data=data)
            print(response.get_json())
            assert response.status_code == 200
            assert 'accuracy' in response.get_json()
            assert 'f1' in response.get_json()


# def test_download_invalid_model(client_svc):
#     with patch('apis.api.auth_check', return_value=True):
#         with patch(const_patch) as mock_app:
#             instance = mock_app.return_value
#             instance.download.return_value = None
#             response = client_svc.get('/model/download/wrong_model')
#             assert response.status_code == 404


# Validate without dataset
def test_validate_without_dataset(client_svc):
    with patch('apis.api.auth_check', return_value=True):
        with patch(const_patch) as mock_app:
            instance = mock_app.return_value
            instance.validate.return_value = ('accuracy', 'f1')
            data = {
                'model': (open(const_model_path, 'rb'), 'model.mdl')
            }
            response = client_svc.post('/model/validate', content_type=const_content_type, data=data)
            assert response.status_code == 404


# Validate with model name in params: /model/validate?model=model
def test_validate_with_model_name(client_svc):
    with patch('apis.api.auth_check', return_value=True):
        with patch(const_patch) as mock_app:
            instance = mock_app.return_value
            instance.validate.return_value = ('accuracy', 'f1')
            data = {
                'dataset': (open(const_dataset_path, 'rb'), const_dataset)
            }
            response = client_svc.post('/model/validate?model=model', content_type=const_content_type, data=data)
            print(response.get_json())
            assert response.status_code == 200
            assert 'accuracy' in response.get_json()
            assert 'f1' in response.get_json()


# Validate with wrong model name in params: /model/validate?model=wrong_model
def test_validate_with_wrong_model_name(client_svc):
    with patch('apis.api.auth_check', return_value=True):
        with patch(const_patch) as mock_app:
            instance = mock_app.return_value
            instance.validate.return_value = ('accuracy', 'f1')
            data = {
                'dataset': (open(const_dataset_path, 'rb'), const_dataset)
            }
            response = client_svc.post('/model/validate?model=wrong_model', content_type=const_content_type, data=data)
            assert response.status_code == 404
