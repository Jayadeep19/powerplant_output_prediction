export PIPENV_VENV_IN_PROJECT := 1


env_setup:
	@echo 'Building python environment for the project...'
	pip install pipenv
	pipenv install --python 3.11
	pipenv run python ./src/get_data.py

mlflow:
	@echo 'Running mlflow server' 
	pipenv run mlflow server --backend-store-uri sqlite:///backend.db --default-artifact-root ./artifacts_local

prefect:
	@echo 'Running prefect server'
	pipenv run prefect server start
	

deployment:
	@echo 'Deploying workflow using pool with prefect and yaml file'
	pipenv run prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
	pipenv run prefect work-pool create --type process without_monitoring_pool
	pipenv run prefect deploy --name train_output_predictor
	pipenv run prefect worker start --pool 'without_monitoring_pool'
	@echo 'Now run the deployment from gui'

web_service:
	@echo 'Preparing the model for webservice deployment'
	@echo 'open the terminal and run cd web_service'
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv install python=3.11
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv shell
	pipenv run python predict.py
	@echo 'Now open another terminal and run test.py'

reset:
	@echo this cleans the entire project
	rm -rf __pycache__
	rm -rf data
	rm -rf mlruns
	rm -rf artifacts_local
	rm -rf backend.db
	pipenv --rm
	rm -rf .venv
 



