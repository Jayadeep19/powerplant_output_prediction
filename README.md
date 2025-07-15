# Power plant Output Prediction
- This project is based on the dataset by [UCIML](https://archive.ics.uci.edu/dataset/294/combined+cycle+power+plant) and [download](https://archive.ics.uci.edu/static/public/294/combined+cycle+power+plant.zip)


## Setup and Usage
### 1. Making environment
- To prepare the environment run: __make env_setup__ 
    ```
    env_setup:
        @echo 'Building python environment for the project...'
        pip install pipenv
        pipenv install --python 3.11
        pipenv run python ./src/get_data.py
    ```

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