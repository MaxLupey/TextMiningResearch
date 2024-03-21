import requests

url = 'http://127.0.0.1:8080/model/train'

file_path = '../tests/test_data/dataset.csv'

files = {'dataset': open(file_path, 'rb')}
response = requests.post(url, files=files)

if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.status_code, response.text)
