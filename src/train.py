import pickle
import pandas as pd
from pathlib import Path
#import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import root_mean_squared_error

import mlflow
from mlflow.tracking import MlflowClient
from prefect import task, flow

import variables as var
from register_model import register_model

@task(name = "reading pickle files")
def read_pkl(file_path):
    with open(file_path, "rb") as f_in:
        return pickle.load(f_in)

@task(name = "prep data")
def prep_data(df:pd.DataFrame, dv:DictVectorizer, fit_dv:bool = False):
    dicts = df[var.categorical_features + var.numerical_features].to_dict(orient='records')
    if fit_dv:
        df = dv.fit_transform(dicts)
    else:
        df = dv.transform(dicts)
    return df, dv

@task(name = "preparing data for training")
def run_data_prep():
    X_train, y_train = read_pkl(var.TRAIN_DATA_PATH)
    X_val, y_val = read_pkl(var.VAL_DATA_PATH)
    X_test, y_test = read_pkl(var.TEST_DATA_PATH)


    dv = DictVectorizer()
    X_train, dv = prep_data(X_train, dv, fit_dv=True)
    X_val, _ = prep_data(X_val, dv)
    X_test, _ = prep_data(X_test, dv)

    return X_train, y_train, X_val, y_val, X_test, y_test, dv

@task(name = "training model")
def train_model(
        dv:DictVectorizer,
        X_train:pd.DataFrame,
        y_train:pd.Series,
        X_val:pd.DataFrame,
        y_val:pd.Series,
):
    """- Train a Random forest regressor using train and val data
    - Log the model and metrics to MLflow
    - #TODO: Create an evidently report for the training
    """

    with mlflow.start_run():
        params = var.model_params
        mlflow.set_tag("model", 'random_forest_regressor_test')
        mlflow.log_params(params)
    
        rfr = RandomForestRegressor(**params)
        rfr.fit(X_train, y_train)
        y_pred = rfr.predict(X_val)
        rmse = root_mean_squared_error(y_val, y_pred)

        mlflow.log_metric("rmse", rmse)
        Path("models").mkdir(exist_ok=True)
        with open("models/dict_vect.bin", "wb") as f_out:
            pickle.dump(dv, f_out)
        mlflow.log_artifact("models/dict_vect.bin", artifact_path="dict_vectorizer")
        signature = mlflow.models.infer_signature(X_train, y_train)
        mlflow.sklearn.log_model(rfr, name="rfr_model_test", signature=signature)
    return None

@flow(name = "training model")
def main():
    mlflow_client = MlflowClient(tracking_uri = var.MLFLOW_TRACKING_URI)
    mlflow.set_tracking_uri(var.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(var.MLFLOW_EXPERIMENT_NAME)
    print("Preparing data for training")
    X_train, y_train, X_val, y_val, X_test, y_test, dv = run_data_prep()
    print("training and logging model")
    train_model(dv, X_train, y_train, X_val, y_val)

    #get the runid of the model and register the model to model registry
    register_model(mlflow_client)

    



if __name__ == '__main__':
    main()
    