import pandas as pd 
import numpy as np 
from datetime import datetime, timedelta
import argparse
from dotenv import load_dotenv
import os
from tqdm import tqdm
from sklearn.metrics import classification_report

from service.feature_encoder.sb_feature_encoder import SBEncoder
from t.utils.service_connector import ServiceConnector
from train_worfklow import train_model

if __name__ == "__main__":
    
    # Add parser for the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--beta", type=int, required=False, default=1)
    parser.add_argument("-e", "--env", type=str, required=False, default="test_env")
    parser.add_argument("-o", "--output", type=str, required=False, default="res")
    
    args = parser.parse_args()
    
    # Load variables for the models 
    load_dotenv(args.env)
    
    beta = args.beta 
                    
    # Service connector
    service_connector = ServiceConnector(os.environ["SERVICE_HOST"], os.environ["SERVICE_PORT"])
            
    st = pd.to_datetime(datetime(2024, 2, 1), utc=True).tz_convert('Asia/Tokyo')
    et = pd.to_datetime(datetime(2024, 2, 3), utc = True).tz_convert('Asia/Tokyo')
            
    pred = []
    true = []
    inf_time = []
    
    for day in tqdm(pd.date_range(st, et, freq = f"{beta}D").to_pydatetime()):
                        
        test_data, t, e = service_connector.fetch_data(st=day, et= day + timedelta(days=beta), feat = "adt") #df[(df.day >= d) & (df.day < d + timedelta(days=beta))]
                     
        if len(test_data) == 0:
            continue
                        
        for idx, job_data in enumerate(test_data):
                        
            pred_class, i_t, e = service_connector.predict(job_data)
                        
            if not(e):          
                print(i_t)
                pred.append(pred_class[0])
                true.append(service_connector.characterise_jobs(test_data[idx]))
                inf_time.append(float(i_t))
            else:
                print(f"ERROR TEST: {e}")
                continue 
    
    with open(os.path.join(args.output, f"results_{str(et.date())}.txt"), "w") as f:
        f.write("Total inference time: {}, Average inference time {:.2f}, Number of Jobs: {}\n".format(sum(inf_time), np.mean(inf_time), len(pred)))
        f.write(classification_report(true, pred))
        
            
        
        
    
    
    
    
    