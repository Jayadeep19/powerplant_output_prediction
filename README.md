# Power plant Output Prediction
- This project is based on the dataset by [UCIML](https://archive.ics.uci.edu/dataset/294/combined+cycle+power+plant) and [download](https://archive.ics.uci.edu/static/public/294/combined+cycle+power+plant.zip). The dataset has 9568 datapoints from a combined power plant. The dataset is clean and has no nan or empty data rows. There are 5 features which are;

1. AT: Ambient temperature
2. V: Exhaust vaccum
3. AP: Ambient pressure
4. RH: Relative humidity
5. EP: Electrical energy output.

In this project the aim is to predict the energy output of the powerplant. The first 4 are used to predict the Electrical energy output. Finally, the trained model is made available as a webservice so that it serves as a initial predictor for the powerplant workers to ensure if the power generation is following an expected path or if there is some deeper analysis to be made immediatly.

## Setup and Usage
### 1. Making environment
- To prepare the environment run: __make env_setup__ (_python3.11_ is required for successful installation)
    ```
    env_setup:
        @echo 'Building python environment for the project...'
        pip install pipenv
        pipenv install --python 3.11
        pipenv run python ./src/get_data.py
    ```
    The dataset need not be downloaded manually. Running the above command will both create the virtual environment required with the dataset downloaded, unzipped and sorted to `data` folder
### 2. Start tracking server using mlflow
- For mlflow: __make mlflow__  
    ```
    mlflow:
        @echo 'Running mlflow server'
        mlflow server --backend-store-uri sqlite:///backend.db --default-artifact-root ./artifacts_local 
    ```
    the mlflow GUI can be accessed at http://127.0.0.1:5000

### 3. start a prefect server
- To start a prefect server: __make prefect__
    ```
    prefect:
	@echo 'Running prefect server'
	pipenv run prefect server start
	pipenv run prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
    ```

### 4. Automatically deploy the workflow to prefect server
- Run: __make deployment__
    ```
    @echo 'Deploying workflow using pool with prefect and yaml file'
	pipenv run prefect work-pool create --type process without_monitoring_pool
	pipenv run prefect deploy --name train_output_predictor
	pipenv run prefect worker start --pool 'without_monitoring_pool'
	@echo 'Now run the deployment from gui'
    ```
    This will create a work pool named __without_monitoring_pool__ and deploy the workflow as __train_output_predictor__ as described in the prefect.yaml file. Later also starts a prefect worker for this workpool. Aow head over to the prefect server and press `quick run` on the deployment.

### 5. Make the ml model available as webservice
- Run: __make web_service__
    ```
    @echo 'Preparing the model for webservice deployment'
	@echo 'open the terminal and run cd web_service'
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv install python=3.11
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv shell
	pipenv run python predict.py
	@echo 'Now open another terminal and run test.py
    ```
    Running the above command created a seperate virtual environment inside the project's virtual environment and installs all the dependencies. And also it uses flask to host the model and makes it available at http://0.0.0.0:9696. Now open another window and run test.py to send a request to the webpage to get a prediction.

### 6. Clean the project
- Run: ___make reset_
    ```
    @echo cleaning the project directory
    rm -rf __pycache__
	rm -rf data
	rm -rf mlruns
	rm -rf artifacts_local
	rm -rf backend.db
	pipenv --rm
    ```
    Running this command will clean the entire project directory and sets it to the former condition. Note: This also removes the __virtual_environment__ also