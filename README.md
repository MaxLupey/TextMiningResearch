[![codecov](https://codecov.io/gh/MaxLupey/TMining/graph/badge.svg?token=V7V942KO1A)](https://codecov.io/gh/MaxLupey/TMining)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MaxLupey_TMining&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=MaxLupey_TMining)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/MaxLupey/TMining/blob/main/LICENSE)
[![CodeQL](https://github.com/MichaelCurrin/badge-generator/workflows/CodeQL/badge.svg)](https://github.com/MaxLupey/TMining/actions?query=workflow%3ACodeQL "Code quality workflow status")



A repository for text mining [scientific](https://scholar.google.com/citations?hl=en&user=8_OPWxAAAAAJ) research. This app is suitable for text mining research like news reliability (fake news) detection, authorship, and unique text style detection.


![data-science-methodology](https://github.com/MaxLupey/TMining/assets/55431857/5543f7ba-a4b6-4606-bc1e-06f4d87a1a25)

# TMining
TMining is a Python library designed for text analysis and sentiment detection, leveraging the powerful scikit-learn library for simplicity and extensibility. Additionally, this repository is specifically crafted to detect fake news based on a developed model.

### Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Register Google OAuth API](#register-google-oauth-api)
- [Download Datasets](#download-datasets)
- [Commands](#commands)
  * [Training](#training)
  * [Validation](#validation)
  * [Predictions](#predictions)
  * [Vizualization](#vizualization)
  * [Hosting](#hosting)
    + [Requests](#requests)

This model processes textual input and generates a binary output of 0 or 1, where 0 might indicate the potential presence of fake content, while 1 could suggest its potential truthfulness. This capability allows for swift and automated analysis of news content for its potential credibility.
## Installation
> [!NOTE]
> **For proper operation of the application, [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html), [git](https://git-scm.com/downloads) and [Node JS](https://nodejs.org/en/download) must be installed in the default path.**

Once the repository is cloned, follow these steps for installation:

1. Navigate to the cloned repository.
2. Run
```bash
# Create a conda environment
conda env create -f ./backend/env/tmining.yml
```
> [!NOTE]
> In case you need to remove the conda server, use the script below:  
> **conda env remove --name tmining**

3. After installation, activate the environment using:

```bash
# Activate the conda environment
conda activate tmining
```
> [!NOTE]
> In case you need to deactivate an active environment, use the script below:  
> **conda deactivate**

4. To start Flask and React programs, you need to use one of the scripts, for Windows: 
```cmd
start.bat
```
and for Linux/macOS: 
```bash
./start.sh
```

> [!CAUTION]
> Register Google OAuth API for your application before running it.

## Configuration
Configuration host for React application is located in the `./frontend/src/api/routers/tminingRouters.ts` file. You need to change the `tminingUrl` variable to the address of the server where the Flask application is running. By default, the address is `http://localhost:5000`.

```typescript
const tminingUrl = "http://localhost:5000";
```

Configuration host for Flask application is located in the `./backend/config.py` file. You need react_app to change right url to the address of the server where the React application is running. By default, the address is `http://localhost:3000`.

```python
react_app = "http://localhost:3000"
```
## Register Google OAuth API
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.

![Google Cloud Console](https://github.com/MaxLupey/TextMining/assets/80894944/1743fedb-da48-450a-aebe-a1e633412f09)
![Create Project](https://github.com/MaxLupey/TextMining/assets/80894944/806b4fba-a882-49db-a006-ab1850afad00)
![Creating Project](https://github.com/MaxLupey/TextMining/assets/80894944/1e88ec3b-5bb9-44c9-aae5-b623dfdd75db)
3. In the sidebar on the left, expand APIs & Services and select OAuth consent screen.

![Select User Type](https://github.com/MaxLupey/TextMining/assets/80894944/a16f90bc-b7f1-46f1-a078-ee05ac625f8d)
4. Choose an email address, enter a product name and click the Save button.

![Filling in information](https://github.com/MaxLupey/TextMining/assets/80894944/080ab38a-cc07-42b5-b66b-29bfd26b6704)
5. In the sidebar on the left, select Credentials. Click the Create credentials button and select OAuth client ID.

![Credentials](https://github.com/MaxLupey/TextMining/assets/80894944/621a4a6a-83d6-4a1e-929a-23d8eed07f1e)
6. Select the application type Web application. Enter the name of the application, and the authorized redirect URIs. Format: `http://localhost:5000/callback`

![Creating OAuth client ID](https://github.com/MaxLupey/TextMining/assets/80894944/8f2aa887-dc4e-4a6d-a23f-095d2f14f980)
7. After creating the OAuth client, click the Download JSON button to download the client_secret file.

![Download JSON](https://github.com/MaxLupey/TextMining/assets/80894944/ac0e5bc9-7992-4591-a664-7946a9f1e7a4)
8. Move the downloaded file to the `./backend/env` directory and rename it to `client_secrets.json`.

## Download Datasets
The datasets that we use for training and testing our models are located on Zenodo's third-party server (https://zenodo.org/records/10359504). To download these datasets, you need to run the following script:
```bash
zenodo_get https://zenodo.org/records/10359504 -o ./data  
```
The datasets will be located in the ./data folder, which will be automatically created when the script is run.
In total, we used three datasets:
- `liar.csv` - the first dataset
- `factcheck.csv` - the second dataset
- `politifact.csv` - the third dataset



## Commands
- `train` - Trains a machine learning model using the provided dataset and saves it to a file.
- `validate` - Validate the model using the provided dataset.
- `predict` - Uses a trained model to make a prediction for a given text input.
- `visualize` - Generates an HTML visualization of model predictions for a given text input.
- `host` - host API for model prediction and visualization.
> [!NOTE]
> If you want to know the command syntax, after one of the commands, enter `[-h]` or `[--help]`
## Training
Trains a machine learning model using the provided dataset and saves it to a file.
```bash
python main.py train -dataset_path ./data/factcheck.csv [-x text] [-y target] [-save_to ./result] [-model SVC] [-vectorizer TfidfVectorizer] [-kfold 10] [-test_size 0.2]
```

| Parameter    | Explanation                                                                                                                                                         |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| dataset_path | path to the dataset                                                                                                                                                 |
| x            | name of the column containing the input text. Default: `text`                                                                                                       |
| y            | name of the column containing the output labels. Default: `target`                                                                                                  |
| save_to      | the path of saving the trained model file. Default: the path where the program starts. Default model name: `model.mdl`                                              |
| model        | select a training model. Three models are available: `SVC`, `SVR`, and `LogisticRegression`. Default model: `SVC`                                                   |
| vectorizer   | select the text vectorization. Three approaches are available. `CountVectorizer`, `TfidfVectorizer`, and `HashingVectorizer`. Default vectorizer: `TfidfVectorizer` |
| kfold        | number of folds to use for cross-validation. Default: `1`                                                                                                           |
| test_size    | size of the test set. The test size must be at least `0.0` and less than `1.0`. Default: `0`                                                                        |

> [!WARNING]
> If the `-test_size` parameter is zero, then the accuracy and f1 are not displayed


## Validation
Validate the model using the provided dataset.
```bash
python main.py validate -model_path ./model.mdl -dataset_path ./data/factcheck.csv [-x text] [-y target] [-test_size 0.2]
```

| Parameter    | Explanation                                                                                               |
|--------------|-----------------------------------------------------------------------------------------------------------|
| model_path   | path to the trained model                                                                                 |
| dataset_path | path to the dataset                                                                                       |
| x            | name of the column containing the input text. Default: `text`                                             |
| y            | column name containing the output labels. Default: `target`                                               |
| test_size    | size of the test set. The test size must be greater than `0.0` and not greater than `1.0`. Default: `0.2` |

Example response:

![image](https://github.com/MaxLupey/TextMining/assets/152855049/be5b207f-6e2d-4ede-909f-3c433c9a36e8)

## Predictions
Make predictions for input text using our trained model.
```bash
python main.py predict -model_path ./model.mdl -text "fake news text"
```

| Parameter  | Explanation               |
|------------|---------------------------|
| model_path | path to the trained model |
| text       | text to predict           |

Example response:

![image](https://github.com/MaxLupey/TextMining/assets/152855049/fef5711f-8a86-4c7c-b6d8-013010c326eb)

## Vizualization
Generate an HTML visualization of model predictions for a given text input.
```bash
python main.py visualize -model_path ./model.mdl -text "fake news text" [-features 60] [-save_to ./result.html]
```

| Parameter  | Explanation                                                        |
|------------|--------------------------------------------------------------------|
| model_path | path to the trained model                                          |
| text       | text to visualise the prediction                                   |
| features   | the maximum number of tokens displayed in the table. Default: `40` |
| save_to    | save the rendered results in HTML. Default: `./results/1.html`     |

Example response:

![image](https://github.com/MaxLupey/TextMining/assets/152855049/7cc1f299-b6eb-4c87-9f7d-efce5f0be2cb)


## Hosting
Run the model as a REST-full API service to interact with models
```bash
python main.py host -model_path ./model.mdl [-address 0.0.0.0] [-port 5000] [-model_dir ./tmp]
```


| Parameter  | Explanation                                               |
|------------|-----------------------------------------------------------|
| model_path | path to the trained model                                 |
| address    | IP address for the API host. Default: `0.0.0.0`           |
| port       | port for the API host. Default: `5000`                    |
| model_dir  | path to the directory for saving models. Default: `./tmp` |


> [!WARNING]
> SVR model will not be able to visualize the model, so the /visualize GET request will not work


After launching the API, you can use HTTP requests to interact with the model.

## Requests:

> [!WARNING]
> 1. The trained model will be searched in the directory whose path is specified in the `-model_dir` parameter when running the `host` script. 
>
>2. If the trained model is not found, the model whose path you specified in the `-model_path` parameter when running the `host` script will be used. 
>
>3. In some endpoints, the trained model can be sent manually.


### 1) Train

- `POST /model/train` - Train the model using uploaded user's dataset.
- Parameters:
    - `name` - Name of the trained model.
    - `x` - Name of the column containing the input text. Default: `text`                                                                                                      
    - `y` - Name of the column containing the output labels. Default: `target`                                                                                                 
    - `vectorizer` - Select the text vectorization. Three approaches are available. `CountVectorizer`, `TfidfVectorizer`, and `HashingVectorizer`. Default vectorizer: `TfidfVectorizer`
    - `model` - Name of the machine learning model to use. Three models are available: `SVC`, `SVR`, and `LogisticRegression`. Default model: `SVC`
    - `kfold` - Number of folds to use for cross-validation. Default: `1`                                                                                                          
    - `test_size` - Size of the test set. The test size must be at least `0.0` and less than `1.0`. Default: `0`
- Body:
  - `dataset` - Dataset file

> [!WARNING]
> If the `-test_size` parameter is zero, then the accuracy and f1 are not displayed

```
POST http://localhost:5000/model/train?text=This is a test
```

Example response:

```bash
#JSON
{
  "accuracy": 0.8297377326565144,
  "f1": 0.8626514246715576,
  "link": "http://localhost:5000/model/download/20231228161930"
}
```

### 2) Download

- `GET /model/download/<model_name>` - Download the trained model.
- Parameters:
    - `model_name` - Name of the trained model to be downloaded


```
GET http://localhost:5000/model/download/20231228161930
```

### 3) Validation

- `POST /model/validate` - Validate the model using uploaded user's dataset.
- Parameters:
    - `x` - Name of the column containing the input text. Default: `text`                                                                                                      
    - `y` - Name of the column containing the output labels. Default: `target`                                                                                                 
    - `model` - Name of the trained model to be used for validation
    - `test_size` - Size of the test set. The test size must be greater than `0.0` and not greater than `1.0`. Default: `0.2` 
- Body:
  - `dataset` - Dataset file
  - `model` - Trained model file (optional)

```
POST http://localhost:5000/model/validate
```

Example response:

```bash
#JSON
{
  "accuracy": 0.8297377326565144,
  "f1": 0.8626514246715576,
}
```

### 4) Predictions

- `GET /model/predict` - Make a prediction for a given text input
- Parameters:
    - `model` - Name of the trained model to be used for prediction.
    - `text` - Text to predict


```
GET http://localhost:5000/model/predict?text=This is a test
```

Example response:                                                  

```bash
#JSON
{
  "prediction": "[1]",
  "text": "this is a test"
}
```

### 5) Visualization

- `GET /model/visualize` - Generate an HTML visualization of model predictions for a given text input
- Parameters:
    - `model` - Name of the trained model to be used to visualize of prediction.
    - `text` - Text to visualise the prediction

```
GET http://localhost:5000/model/visualize?text=This is a test
```

Example response: 

<img width="1237" alt="image" src="https://github.com/MaxLupey/TextMining/assets/55431857/d33c48fd-97ed-4efc-a4de-ec73a9613b1b">
