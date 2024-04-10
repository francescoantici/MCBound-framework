import os
from flask import Blueprint, request
from time import time 
from dependency_injector.wiring import inject, Provide

from schema.requests.predict import PredictRequestValidator
from models.containers import Container
from service.classification_model.classification_model import IClassificationModel
from service.feature_encoder.feature_encoder import IFeatureEncoder
from service.job_characteriser.job_characteriser import IJobCharacteriser

classification_model_api = Blueprint("classification_model", __name__, url_prefix="/classification_model")

@classification_model_api.post("/predict")
@inject
def predict(classification_model: IClassificationModel = Provide[Container.classification_model], feature_encoder: IFeatureEncoder = Provide[Container.feature_encoder], job_characteriser: IJobCharacteriser = Provide[Container.job_characteriser]):
    try:
        req = request.get_json()
        PredictRequestValidator.validate_request(req)
        jobs_data = req["jobs_data"]
        t0 = time.time()
        encoded_job_data = feature_encoder.encode(jobs_data)
        pred_classes = classification_model.predict(encoded_job_data)
        t1 = time.time()
        return {"pred_classes":list(map(job_characteriser.idx2lbl, pred_classes)), "inference_time": "{:.2f}".format(t1-t0), "error":None}, 200
    except Exception as e:
        return {"pred_classes":[], "inference_time":None, "error":str(e)}, 500

@classification_model_api.post("/update")
@inject
def update(classification_model: IClassificationModel = Provide[Container.classification_model]):
    try:
        t0 = time.time()
        classification_model.update(os.environ["MODEL_WEIGHTS_PATH"])
        t1 = time.time()
        return {"reload_time": "{:.2f}".format(t1-t0), "error":None}, 200
    except Exception as e:
        return {"reload_time":None, "error":str(e)}, 500