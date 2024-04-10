import requests

class ServiceConnector:
    
    def __init__(self, address):
        self.address = address

    def predict(self, job_data):
        if type(job_data) != list:
            job_data = [job_data]
        res = requests.post(f"{self.address}/classification_model/predict", json = {"jobs_data":job_data}).json()
        return res["pred_classes"], res["inference_time"], res["error"]
    
    def chracterize(self, job_data):
        res = requests.post(f"{self.address}/characterize", json = {"jobs_data":[job_data]}).json()
        return res["classes"], res["inference_time"], res["error"]

    def update_model(self, stage = "prod"):
        res = requests.post(f"{self.address}/classification_model/update", json = {"stage":stage}).json()
        return res["reload_time"], res["error"]
    
    def fetch_data(self, st, et, feat):
        res = requests.post(f"{self.address}/fetch_data", json = {"start_time":str(st), "end_time":str(et), "feature":feat}).json()
        return res["jobs_data"], res["inference_time"], res["error"]