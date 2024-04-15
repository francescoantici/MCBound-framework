import numpy as np
from datetime import datetime, timedelta
import os
import time

from service.classification_model.knn import KNN
from service.classification_model.classification_model import IClassificationModel
from service.feature_encoder.sb_feature_encoder import SBEncoder
from service.feature_encoder.feature_encoder import IFeatureEncoder
from service.job_characterizer.fugaku_job_characterizer import FugakuJobCharacterizer
from service.job_characterizer.job_characterizer import IJobCharacterizer
from service.data_fetcher.data_fetcher import IDataFetcher
from service.data_fetcher.fugaku_data_fetcher import FugakuDataFetcher
from utils.log_utils import write_log
               
def train_model(st:datetime, et:datetime, feature_encoder:IFeatureEncoder = SBEncoder, job_characteriser:IJobCharacterizer = FugakuJobCharacteriser, data_fetcher:IDatafetcher = FugakuDataFetcher, classification_model:IClassificationModel = KNN, model_weights_path:str = "saved_model", logging_path:str = None) -> bool:
    """_summary_

    Args:
        service_url (str): Url of the MCBound instance.
        st (datetime): Start time to fetch jobs.
        et (datetime): End time to fetch jobs.
        feature_encoder (IFeatureEncoder): Feature encoder model to encode the job data.
        job_characteriser (IJobCharacterizer): Characterizer for the jobs.
        classification_model (IClassificationModel) Instance of the classification model to train
        model_weights_path (str): Path to save the model weights to be used from MCBound.
        logging_path (str, optional): Path to the log. Defaults to None.

    Returns:
        bool: False if execeptions raised, True otherwise.
    """
    try:
            
        # Fetching job data for training        
        job_data = data_fetcher().fetch(st=st, et= day, feat = "edt")
        
        # Training timer
        t0_tot = time.time()
        
        # Model initialization
        cmi = classification_model()
        
        # Training data creation 
        encoded_job_data = feature_encoder().encode(jobs_data)
        classes = np.array(job_characteriser().characterise_jobs(jobs_data))
            
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
            write_log(os.path.join(logging_path, "log"), f"[{str(datetime.now())}] Total Training time: {str(tot_time_train)}, Model Training Time: {str(time_train)}, Total train data: {len(classes)}, Memory-bound: {len(classes[classes == 'memory-bound'])}, Compute-bound: {len(classes[classes == 'compute-bound'])}\n")
    except Exception as e:
        if logging_path:
            # Logging of training operation
            write_log(os.path.join(logging_path, "log"), f"Error: {e}")
        return False
    else:
        return True
        

            
    
    
    
    
    
    
    