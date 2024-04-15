import numpy as np
import pandas as pd 
from datetime import datetime, timedelta
import seaborn as sns 
import matplotlib.pyplot as plt 
import os
import time

from service.data_fetcher.fugaku_data_fetcher import FugakuDataFetcher
from service.job_characterizer.fugaku_job_characterizer import FugakuJobCharacterizer
from utils.plot_roofline import roofline

if __name__ == "__main__":
        
    # Characterization period
    st = pd.to_datetime(datetime(2023, 12, 1), utc=True).tz_convert('Asia/Tokyo')
    et = pd.to_datetime(datetime(2024, 2, 29), utc = True).tz_convert('Asia/Tokyo')
    
    # Data fetcher for Fugaku jobs 
    data_fecther = FugakuDataFetcher()
    
    # Fetch jobs executed between December 23 and February 24
    jobs_data = data_fecther.fetch(st, et, "edt")
    
    # Parse job data into Dataframe
    df_jobs = pd.DataFrame.from_records(jobs_data)
    
    # Characterize job data
    job_characterizer = FugakuJobCharacterizer()
    
    df_jobs["Label"] = job_characterizer.characterize_jobs(jobs_data)
    
    # Save dataset 
    df.to_parquet("characterized_job_data.parquet", index = False)
    
    # Count labels distribution
    label_count = {l:f"{l} ({len(df[df.Label == l])})" for l in df.Label.unique()}
    
    # Modify labels for visualization purposes
    df_jobs["Label (# of jobs)"] = df_jobs.Label.apply(new_labels.get)
    df_jobs["Frequency (GHz) (# of jobs)"] = df_jobs["cr_str_freq"].apply(new_labels.get)
    
    # Plot roofline model with the job data
    roofline(df_jobs, job_characterizer.TOP_PERF, job_characterizer.TOP_BM, hue="Label (# of jobs)", save_path="plots")
    
    # Plot roofline by distinguishing job run frequency      
    roofline(df_jobs, job_characterizer.TOP_PERF, job_characterizer.TOP_BM, hue="Frequency (GHz) (# of jobs)", save_path="plots")
    
    
    
    
        

            
    
    
    
    
    
    
    