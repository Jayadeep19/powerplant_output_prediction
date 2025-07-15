from prefect import flow

import predict
import train


@flow(name = 'main flow')
def main_flow():

    client, X_test, y_test = train.main()
    data = X_test["EP"] = y_test
    predictions = predict.predict(mlflow_client=client, data = data)
    print(f"Some of the predictions are {predictions[3]}")
    pass