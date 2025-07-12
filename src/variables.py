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
VAL_DATA_PATH = DATA_PATH.joinpath('processed_data','valid.pkl')

#ml model variables
model_dir = PROJECT_DIR.joinpath('models')

target = "PE"
features = ['AT', 'V', 'AP', 'RH']
