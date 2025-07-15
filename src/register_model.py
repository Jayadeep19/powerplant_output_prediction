

import mlflow
from mlflow.entities import ViewType
from prefect import task, flow

import variables as var

@task(name = 'registering model to mlflow model registry', log_prints= True)
def register_model(mlflow_client):
    """"This function searches the runs in the given mlflow experiment that the client is associated with and registers the model."""
    
    runs = mlflow_client.search_runs(
        experiment_ids=1,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=1,
    )[0]
    run_id = runs.info.run_id
    model_uri = f"runs:/{run_id}/rfr_model_test"

    registered_models = mlflow.search_registered_models()
    if not registered_models:
        mlflow.register_model(model_uri=model_uri, name= var.MLFLOW_MODEL_NAME)
        print("Model has been registered to the model registry")
        var.REGISTERED_MODEL["run_id"] = run_id
        var.REGISTERED_MODEL["model_uri"] = model_uri
    else:
        for model in registered_models:
            if model.name == var.MLFLOW_MODEL_NAME:
                if model.latest_versions:
                    for mv in model.latest_versions:
                        if mv.run_id == run_id:
                            print("The model is already registered to the model registry")
                mlflow.register_model(model_uri=model_uri, name= var.MLFLOW_MODEL_NAME)
                print("model with the same name is already registered, registering a new version")
                var.REGISTERED_MODEL["run_id"] = run_id
                var.REGISTERED_MODEL["model_uri"] = model_uri
