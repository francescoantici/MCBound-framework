from flask import Blueprint, request
import time
from dependency_injector.wiring import inject, Provide

from schema.requests.characterize import CharacterizeRequestValidator
from models.containers import Container
from service.job_characterizer.job_characterizer import IJobCharacterizer

characterize_api = Blueprint("characterize", __name__, url_prefix="/characterize")

@characterize_api.post("/")
@inject
def characterize(job_characterizer: IJobCharacterizer = Provide[Container.job_characterizer]):
    try:
        req = request.get_json()
        CharacteriseRequestValidator.validate_request(req)
        t0 = time.time()
        classes = job_characterizer.characterise(req["jobs_data"])
        t1 = time.time()
        return {"classes":classes, "inference_time": "{:.2f}".format(t1-t0), "error":None}, 200
    except Exception as e:
        return {"classes":[], "inference_time":None, "error":str(e)}, 500