import os
from flask import Blueprint, request
import time
from dependency_injector.wiring import inject, Provide
from dependency_injector import providers

from schema.requests.predict import PredictRequestValidator
from schema.requests.update import UpdateRequestValidator
from models.containers import Container
from service.classification_model.classification_model import IClassificationModel
from service.feature_encoder.feature_encoder import IFeatureEncoder
from service.job_characterizer.job_characterizer import IJobCharacterizer

classification_model_api = Blueprint("classification_model", __name__, url_prefix="/classification_model")

@classification_model_api.post("/predict")
@inject
def predict(classification_model: IClassificationModel = Provide[Container.classification_model], feature_encoder: IFeatureEncoder = Provide[Container.feature_encoder], job_characterizer: IJobCharacterizer = Provide[Container.job_characterizer]):
    """_summary_
    /classification_model/predict API, takes a series of job data and returns the memory/compute-bound prediction for each of the jobs.
    Args:
        classification_model (IClassificationModel, optional): _description_. Defaults to Provide[Container.classification_model].
        feature_encoder (IFeatureEncoder, optional): _description_. Defaults to Provide[Container.feature_encoder].
        job_characterizer (IJobCharacterizer, optional): _description_. Defaults to Provide[Container.job_characterizer].

    Returns:
        _type_: _description_
    """
    try:
        # Get request
        req = request.get_json()
        
        # Validate request
        PredictRequestValidator.validate_request(req)
        
        # Extract job data
        jobs_data = req["jobs_data"]
        t0 = time.time()
        
        # Encode job data
        encoded_job_data = feature_encoder.encode(jobs_data)
        
        # Generate predictions
        pred_classes = classification_model.predict(encoded_job_data)
        t1 = time.time()
        return {"pred_classes":list(map(job_characterizer.idx2lbl.get, pred_classes)), "inference_time": "{:.2f}".format(t1-t0), "error":None}, 200
    except Exception as e:
        return {"pred_classes":[], "inference_time":None, "error":str(e)}, 500

@classification_model_api.post("/update")
@inject
def update(classification_model: IClassificationModel = Provide[Container.classification_model], config :providers.Configuration = Provide[Container.config]):
    """_summary_
    /classification_model/update API, updates the trained classification model
    Args:
        classification_model (IClassificationModel, optional): _description_. Defaults to Provide[Container.classification_model].
        config (providers.Configuration, optional): _description_. Defaults to Provide[Container.config].

    Returns:
        _type_: _description_
    """
    try:
        # Get request
        req = request.get_json()
        
        # Validate request
        UpdateRequestValidator.validate_request(req)
        
        # Update model
        t0 = time.time()
        classification_model.update(config.model_weights_path, req["stage"])
        t1 = time.time()
        return {"reload_time": "{:.2f}".format(t1-t0), "error":None}, 200
    except Exception as e:
        return {"reload_time":None, "error":str(e)}, 500