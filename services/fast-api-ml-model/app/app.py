import inspect
import bcrypt

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse

from app.models import UserPermission
from app.schema import LogisticRegressionParameters, GradientBoostingClassifier

api = APIRouter()


@api.post("/run/<model_id>")
def train_model(model_id: str,
                model_parameters_logistic: LogisticRegressionParameters = None,
                model_parameters_gb: GradientBoostingClassifier = None):
    if (not model_parameters_logistic) and (not model_parameters_gb):
        return JSONResponse()
    if not UserPermission.find_model_id(model_id=model_id):
        return JSONResponse()

    return {"message", "Saved successfully!"}
