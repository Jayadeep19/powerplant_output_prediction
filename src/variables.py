import os
from pathlib import Path

#data and path variables for the project
PROJECT_DIR = Path(__file__).absolute().parent.parent
URL = "https://archive.ics.uci.edu/static/public/294/combined+cycle+power+plant.zip"
FILES = ['Folds5x2_pp.xlsx', 'Readme.txt']
DATA_PATH = PROJECT_DIR.joinpath('data')
RAW_DAT_PATH = DATA_PATH.joinpath('CCPP', 'Folds5x2_pp.xlsx')
TRAIN_DATA_PATH = DATA_PATH.joinpath('processed_data','train.pkl')
TEST_DATA_PATH = DATA_PATH.joinpath('processed_data','test.pkl')
VAL_DATA_PATH = DATA_PATH.joinpath('processed_data','val.pkl')

#ml model variables
model_dir = PROJECT_DIR.joinpath('models')

target = "PE"
categorical_features = []
numerical_features = ['AT', 'V', 'AP', 'RH']

      # Take randon model params for now, later implement a hyperoptimization strategy
model_params = {"n_estimators": 10,
                "max_depth": 10,
                "min_samples_split": 2,
                "min_samples_leaf": 1,
                "random_state": 42}


#mlflow variables
MLFLOW_TRACKING_URI = 'sqlite:///backend.db'
MLFLOW_EXPERIMENT_NAME = 'powerplant_output_prediction'
MLFLOW_MODEL_NAME = 'pp_output_regression_model'
      # these varaibles are updated during model registry
REGISTERED_MODEL = {"run_id":None,
                    "model_uri":None}