from flask import Blueprint, request
from time import time 
from dependency_injector.wiring import inject, Provide

from schema.requests.characterise import CharacteriseRequestValidator
from models.containers import Container
from service.job_characteriser.job_characteriser import IJobCharacteriser

characterise_api = Blueprint("characterise", __name__, url_prefix="/characterise")

@characterise_api.post("/")
@inject
def characterise(job_characteriser: IJobCharacteriser = Provide[Container.job_characteriser]):
    try:
        req = request.get_json()
        CharacteriseRequestValidator.validate_request(req)
        t0 = time.time()
        classes = job_characteriser.characterise(req["jobs_data"])
        t1 = time.time()
        return {"classes":classes, "inference_time": "{:.2f}".format(t1-t0), "error":None}, 200
    except Exception as e:
        return {"classes":[], "inference_time":None, "error":str(e)}, 500