import numpy as np
import pandas as pd 
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import time
import json 
import argparse
from tqdm import tqdm 

from service.classification_model.knn import KNN
from service.classification_model.rf import RF
from service.data_fetcher.parquet_data_fetcher import ParquetDataFetcher
from service.feature_encoder.sb_feature_encoder import SBEncoder
from service.job_characteriser.fugaku_job_characteriser import FugakuJobCharacteriser

                    
def train_model(jobs_data, feature_encoder, job_characteriser, classification_model, model_weights_path, logging_path = None):
           
    t0_tot = time.time()
    
    cmi = classification_model()
    
    encoded_job_data = feature_encoder.encode(jobs_data)
    classes = np.array(job_characteriser.characterise_jobs(jobs_data))
         
    # Train the model on the newly retrieved data and save the new model to file    
    t0_train = time.time()
    cmi.train(encoded_job_data, classes)
    t1_train = time.time()
    
    t1_tot = time.time()
    
    cmi.save(model_weights_path)
    
    tot_time_train = t1_tot-t0_tot
    time_train = t1_train-t0_train
    
    if logging_path:
        # Logging of training operation
        with open(os.path.join(logging_path, "log.txt"), "a") as f:
            f.write(f"[{str(datetime.now())}] Total Training time: {str(tot_time_train)}, Model Training Time: {str(time_train)}, Total train data: {len(classes)}, Memory-bound: {len(classes[classes == 'memory-bound'])}, Compute-bound: {len(classes[classes == 'compute-bound'])}\n")
    
    return tot_time_train, time_train, tot_time_train-time_train
    
if __name__ == "__main__":
        
    # Add parser for the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--alpha", type=int, required=False, default=15)
    parser.add_argument("-w", "--weights-path", type=str, required=True)
    parser.add_argument("-o", "--output", type=str, required=False, default="res")
    
    args = parser.parse_args()
    
    alpha = args.alpha
    weights_path = args.weights_path 
    output = args.output
        
    # Data fetcher 
    data_fetcher = ParquetDataFetcher("/home/fantici/mem_bound/data_dec_feb.parquet")
        
    # Job characteriser 
    job_characteriser = FugakuJobCharacteriser()
    
    # Feature encoder 
    feature_encoder = SBEncoder()
    
    # Training data st
    st = pd.to_datetime(datetime.now(), utc=True).tz_convert('Asia/Tokyo')
    
    # Fetching training data 
    jobs_data = data_fetcher.fetch(st = st - timedelta(days = alpha), et=st, feat = "edt")
    
    # Training model
    tt, ttr, te = train_model(jobs_data, feature_encoder, job_characteriser, KNN, weights_path, output)
            
    
    
    
    
    
    
    