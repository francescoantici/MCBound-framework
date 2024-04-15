import numpy as np 
from datetime import datetime, timedelta
import argparse
import os
from tqdm import tqdm
from sklearn.metrics import classification_report

from service.characterization.fugaku_job_characterizer import FugakuJobCharacterizer
from service.data_fetcher.fugaku_data_fetcher import FugakuDataFetcher
from service.classification.knn import KNN
from service.feature_encoder.sb_feature_encoder import SBEncoder
from utils.service_connector import ServiceConnector
from utils.log_utils import write_log
from workflows.train_workflow import train_model
from workflows.inference_workflow import inference

if __name__ == "__main__":
    
    # Add parser for the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--service-url", type=str, required=True)
    parser.add_argument("-a", "--alpha", type=int, required=False, default=15)
    parser.add_argument("-b", "--beta", type=int, required=False, default=1)
    parser.add_argument("-l", "--logging", type=str, required=False)
    
    args = parser.parse_args()
    
    # Parameters for the evaluation
    alpha = args.alpha 
    beta = args.beta
    service_url = args.service_url
    logging_path = args.logging
    
    # MCBound instance interface
    service_connector = ServiceConnector(service_url)
    
    # Fugaku data fetcher 
    data_fetcher =  FugakuDataFetcher()
                        
    # Prediction model for the jobs
    classification_model = KNN
    
    # Job characteriser 
    job_characteriser = FugakuJobCharacteriser()
    
    # Feature encoder 
    feature_encoder = SBEncoder()
    
    # Timespan of the evaluation December 23 - February 24
    st = pd.to_datetime(datetime(2024, 2, 1), utc=True).tz_convert('Asia/Tokyo')
    et = pd.to_datetime(datetime(2024, 2, 29), utc = True).tz_convert('Asia/Tokyo')
    
    predicted_values = []
    true_values = []
    inf_time = []
    
    for day in tqdm(pd.date_range(st, et, freq = f"{beta}D").to_pydatetime()):
        try:
            train_model()
            service_connector.update_model()
        except Exception as e:
            write_log(os.path.join(logging_path, "log"), e)
            continue
        
        # Retrieve testing data      
        test_data = data_fetcher.fetch(st=day, et= day + timedelta(days=beta), feat = "adt") 
        
        # If no job data are available the evaluation is skipped          
        if len(test_data) == 0:
            continue
                        
        for idx, job_data in enumerate(test_data):
                        
            pred_class, inf_time, e = service_connector.predict(job_data)
                        
            if not(e):          
                predicted_values.append(pred_class[0])
                true_values.append(service_connector.characterize(test_data[idx]))
                inf_time.append(float(i_t))
            else:
                write_log(os.path.join(logging_path, "log"), e)
                continue 
            
    write_log(os.path.join(logging_path, f"results_{alpha}_{beta}.txt"), "Total inference time: {}, Average inference time {:.2f}, Number of Jobs: {}\n".format(sum(inf_time), np.mean(inf_time), len(predicted_values)))
    write_log(os.path.join(logging_path, f"results_{alpha}_{beta}.txt"), classification_report(true_values, predicted_values))
    
            
        
        
    
    
    
    
    