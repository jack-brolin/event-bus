import inspect
import bcrypt

from fastapi import APIRouter, Depends, Request, status, Body, BackgroundTasks
from fastapi.responses import JSONResponse

from app.schema import LogisticRegressionParameters, GradientBoostingClassifier
from app.ml import run_logistic_regression, run_gbm
from app.utils import check_permission

api = APIRouter()


@api.post("/run/<model_id>")
async def train_model(model_id: str,
                      background_tasks: BackgroundTasks,
                      username: str = Body(None),
                      model_parameters_logistic: LogisticRegressionParameters = None,
                      model_parameters_gb: GradientBoostingClassifier = None):
    if (model_id == 'LogisticRegressionModel') and (not model_parameters_logistic):
        return JSONResponse(content={"message": "Missing LogisticRegression model parameters."}, status_code=400)
    if (model_id == 'GradientBoostingModel') and (not model_parameters_gb):
        return JSONResponse(content={"message": "Missing GradientBoosting model parameters."}, status_code=400)
    if (not model_parameters_logistic) and (not model_parameters_gb):
        return JSONResponse(content={"message": "Missing model parameters."}, status_code=400)

    if not check_permission(username=username, model_id=model_id):
        return JSONResponse(content={"message": "User is not allowed to train this model."}, status_code=400)

    if model_id == "LogisticRegressionModel":
        background_tasks.add_task(run_logistic_regression, model_parameters=model_parameters_logistic)
    elif model_id == "GradientBoostingModel":
        background_tasks.add_task(run_gbm, model_parameters=model_parameters_logistic)
    else:
        return JSONResponse(content={"message": "Model ID not valid."}, status_code=400)
    return JSONResponse(content={"message": "Model training started!"}, status_code=200)
