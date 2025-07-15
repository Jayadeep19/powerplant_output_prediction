import pandas
import pickle
from pathlib import Path

from mlflow.tracking import MlflowClient
from sklearn.metrics import root_mean_squared_error
from prefect import flow

import variables as var

@flow(name = "predicting using model")
def predict(mlflow_client: MlflowClient, data):

    #client = MlflowClient(tracking_uri=var.MLFLOW_TRACKING_URI)
    models = mlflow_client.search_registered_models(filter_string=f"name = '{var.MLFLOW_MODEL_NAME}'")

    (run_id, model_source) = [(model.latest_versions[0].run_id, model.latest_versions[0].source) for model in models][0]

    #load model, dv and test data
    model_uri = f'./mlruns/1/models/{model_source.split("/")[-1]}/artifacts/model.pkl'
    with open(model_uri, 'rb') as f_out:
        model = pickle.load(f_out)
    dv_url = f'./mlruns/1/{run_id}/artifacts/dict_vectorizer/dict_vect.bin'
    with open(dv_url, 'rb') as d_out:
        dv = pickle.load(d_out)
    
    
#   with open(var.TEST_DATA_PATH, "rb") as f:   #for prediction on test data
#       x,y = pickle.load(var.TEST_DATA_PATH)
    if isinstance(data, Path):
        with open(data, "rb") as f:   #for prediction on test data
            test_df_X, test_df_y = pickle.load(f)
    if isinstance(data,pandas.DataFrame):
        test_df_X = data
        test_df_y = data[var.target]
    # predict a part of test data for now.
    dicts = test_df_X[var.categorical_features + var.numerical_features].to_dict(orient='records')
    X_test = dv.transform(dicts)


    # predict using the model
    predictions = model.predict(X_test)

    rmse = root_mean_squared_error(predictions, test_df_y)
    print(f"rmse during testing is: {rmse}")

    #print(predictions)
    return predictions


if __name__ == "__main__":

    client = MlflowClient(tracking_uri=var.MLFLOW_TRACKING_URI)
    
    #data = var.TEST_DATA_PATH

    #data as dataframe: 19.64	48.06	1014.81	74.96 455
    d = {'AT':[20],
        'V':[50],
        'AP': [1015],
        'RH': [75],
        'PE':[450]}
    data = pandas.DataFrame.from_dict(d)
    print(data)
    predict(mlflow_client=client, data = data)
