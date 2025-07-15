export PIPENV_VENV_IN_PROJECT := 1


env_setup:
	@echo 'Building python environment for the project...'
	pip install pipenv
	pipenv install --python 3.11
	pipenv run python ./src/get_data.py

mlflow:
	@echo 'Running mlflow server'
	pipenv run prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api 
	pipenv run mlflow server --backend-store-uri sqlite:///backend.db --default-artifact-root ./artifacts_local

prefect:
	@echo 'Running prefect server'
	pipenv run prefect server start
	pipenv run prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api

deployment:
	@echo 'Deploying workflow using pool with prefect and yaml file'
	pipenv run prefect work-pool create --type process without_monitoring_pool
	pipenv run prefect deploy --name train_output_predictor
	pipenv run prefect worker start --pool 'without_monitoring_pool'
	@echo 'Now run the deployment from gui'


