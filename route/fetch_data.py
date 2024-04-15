from flask import Blueprint, request
import time
from dependency_injector.wiring import inject, Provide
import pandas as pd

from schema.requests.fetch_data import FetchDataValidator
from models.containers import Container
from service.data_fetcher.data_fetcher import IDataFetcher

fetch_data_api = Blueprint("fetch_data", __name__, url_prefix="/fetch_data")

@fetch_data_api.post("/")
@inject
def fetch_data(data_fetcher: IDataFetcher = Provide[Container.data_fetcher]):
    """_summary_
    /fetch_data API, fetches data in a certain timeframe
    Args:
        data_fetcher (IDataFetcher, optional): _description_. Defaults to Provide[Container.data_fetcher].

    Returns:
        _type_: _description_
    """
    try:
        # Get request 
        req = request.get_json()
        
        # Validate request
        FetchDataValidator.validate_request(req)
        
        # Parses timeframe
        st = pd.to_datetime(req["start_time"])
        et = pd.to_datetime(req["end_time"])
        feat = req["feature"]
        
        # Fetch data
        t0 = time.time()
        jobs_data = data_fetcher.fetch(st, et, feat)
        t1 = time.time()
        return {"jobs_data":jobs_data, "inference_time": "{:.2f}".format(t1-t0), "error":None}, 200
    except Exception as e:
        return {"jobs_data":[], "inference_time":None, "error":str(e)}, 500