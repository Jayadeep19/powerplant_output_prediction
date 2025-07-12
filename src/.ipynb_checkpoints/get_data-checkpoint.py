import os

import requests
import zipfile

url = "https://archive.ics.uci.edu/static/public/294/combined+cycle+power+plant.zip"
files = ['Folds5x2_pp.xlsx', 'Readme.txt']


WORKING_DIR = os.getcwd()
DATA_FOLDER = WORKING_DIR + '/data'
ZIP_PATH = DATA_FOLDER+'/dataset.zip'


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