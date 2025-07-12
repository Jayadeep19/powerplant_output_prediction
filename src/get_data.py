import os
import requests
import zipfile
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer

import variables as var

# url = "https://archive.ics.uci.edu/static/public/294/combined+cycle+power+plant.zip"
# files = ['Folds5x2_pp.xlsx', 'Readme.txt']

def dump_pickle(data, filename):
    '''Save the dataset as a pickel file. 
    The data is in the form features, target values'''
    if not os.path.exists(filename.parent):
        os.makedirs(filename.parent)
    with open(filename, 'wb') as f_out:
        pickle.dump(data, f_out)
    pass

def download_dataset(url, files, data_folder):
    '''uses the url and gets the dataset from internet and unzips the required files.'''
    url = var.URL
    files = var.FILES
    DATA_FOLDER = var.DATA_PATH
    ZIP_PATH = DATA_FOLDER.joinpath("dataset.zip")

    os.makedirs(DATA_FOLDER, exist_ok=True)

    #get the zip file from url
    if not os.path.exists(ZIP_PATH):
        print(f"downloading dataset to {DATA_FOLDER}")
        response = requests.get(url)
        if response.status_code == 200:
            with open(ZIP_PATH, 'wb') as file:
                file.write(response.content)
                print("Download completed successfully.")

    #Unzip the file and save csv file in data folder
    if zipfile.is_zipfile(ZIP_PATH):
        print("Unzipping the dataset")
        with zipfile.ZipFile(ZIP_PATH, "r") as zip_file:
            for file in zip_file.namelist():
                if os.path.basename(file) in files:
                    zip_file.extract(file, DATA_FOLDER)
                    print(f"extracted {file}")

def run_data_prep(raw_data_path, dest_path, split_ratio = 0.25):
    '''This function reads the raw dataset and creates individual datasets for train,val and test.
    The default split is 25% for train and test. The validation data is 20% of the train data.'''
    df = pd.read_excel(raw_data_path)
    train_df1, test_df = train_test_split(df, test_size=split_ratio, random_state=42)
    train_df, val_df = train_test_split(train_df1, test_size=0.2, random_state=42)

    target = var.target      #str

    X_train = train_df.drop(columns=[target])
    y_train = train_df[target]

    # Transform the validation and test data
    X_val = val_df.drop(columns = [target])
    y_val = val_df[target]
    
    X_test = test_df.drop(columns = [target])
    y_test = test_df[target]

    # Save the preprocessed data
    dump_pickle((X_train, y_train), dest_path.joinpath('processed_data','train.pkl'))
    dump_pickle((X_val, y_val), dest_path.joinpath('processed_data','val.pkl'))
    dump_pickle((X_test, y_test), dest_path.joinpath('processed_data','test.pkl'))
    print("Data split and save as pickle files")


if __name__ == '__main__':
    data_folder = var.DATA_PATH
    download_dataset(url = var.URL, files = var.FILES, data_folder=data_folder)
    run_data_prep(raw_data_path=var.RAW_DAT_PATH, dest_path=data_folder)
