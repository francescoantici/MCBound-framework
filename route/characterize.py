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
    """_summary_
    /characterize API, takes a series of job data and return their characterizations.

    Args:
        job_characterizer (IJobCharacterizer, optional): _description_. Defaults to Provide[Container.job_characterizer].

    Returns:
        _type_: _description_
    """
    try:
        # Get request
        req = request.get_json()
        
        # Validate request 
        CharacteriseRequestValidator.validate_request(req)
        
        # Characterzation 
        t0 = time.time()
        classes = job_characterizer.characterise(req["jobs_data"])
        t1 = time.time()
        return {"classes":classes, "inference_time": "{:.2f}".format(t1-t0), "error":None}, 200
    except Exception as e:
        return {"classes":[], "inference_time":None, "error":str(e)}, 500