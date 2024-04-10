import pandas as pd 
import numpy as np 
from datetime import datetime, timedelta
import argparse
from dotenv import load_dotenv
import os
from tqdm import tqdm
from sklearn.metrics import classification_report

from service.feature_encoder.sb_feature_encoder import SBEncoder
from utils.service_connector import ServiceConnector
from train_worfklow import train_model

if __name__ == "__main__":
    
    # Add parser for the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--beta", type=int, required=False, default=1)
    parser.add_argument("-u", "--service-url", type=str, required=True)
    parser.add_argument("-o", "--output", type=str, required=False, default="res")
    
    args = parser.parse_args()
    
    # Load variables for the models 
    load_dotenv(args.env)
    
    # Beta value to fetch correct data
    beta = args.beta 
                    
    # Service connector
    service_connector = ServiceConnector(args.service_url)
    
    # Current Datetime formatting        
    et = pd.to_datetime(datetime.now(), utc = True).tz_convert('Asia/Tokyo')
    
    # Fetching new job data          
    test_data, t, e = service_connector.fetch_data(st=day - timedelta(days=beta), et= day, feat = "adt")
    
    # Perform predictions
    pred_class, i_t, e = service_connector.predict(job_data)
    
    # Logging
    with open(os.path.join(args.output, f"results_{str(et.date())}.txt"), "w") as f:
        if e:          
            f.write(f"Error: {e}\n")
        else:
            f.write(f"Total inference time: {i_t}, Average inference time per job {float(i_t)/len(test_data)}, Number of Jobs: {len(test_data)}\n")
    

            
        
            
        
        
    
    
    
    
    