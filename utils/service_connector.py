import requests

class ServiceConnector:
    
    def __init__(self, host, port):
        self.address = f"{host}:{port}"

    def predict(self, job_data):
        print(job_data)
        res = requests.post(f"{self.address}/predict", json = {"jobs_data":[job_data]}).json()
        return res["pred_classes"], res["inference_time"], res["error"]
    
    def chracterise(self, job_data):
        res = requests.post(f"{self.address}/characterise", json = {"jobs_data":[job_data]}).json()
        return res["classes"], res["inference_time"], res["error"]

    def update_model(self):
        res = requests.post(f"{self.address}/update").json()
        return res["reload_time"]
    
    def fetch_data(self, st, et, feat):
        res = requests.post(f"{self.address}/fetch_data", json = {"start_time":str(st), "end_time":str(et), "feature":feat}).json()
        return res["jobs_data"], res["inference_time"], res["error"]