import numpy as np
from datetime import datetime, timedelta
import seaborn as sns 
import matplotlib.pyplot as plt 
import os
import time

from service.data_fetcher.parquet_data_fetcher import ParquetDataFetcher
from service.feature_encoder.sb_feature_encoder import SBEncoder
from service.feature_encoder.feature_encoder import IFeatureEncoder
from service.job_characteriser.fugaku_job_characteriser import FugakuJobCharacteriser
from service.job_characterizer.job_characterizer import IJobCharacterizer

if __name__ == "__main__":
    
    
    
    x = list(range(100000))
    
    mem_line = list(map(lambda i: min(top_perf, mem_bandwidth*i), x))
    
    # sns.scatterplot(data = df, x = "bw", y = "p", hue = "Label")
    # plt.ylabel("Performance (GFLOP/s)")
    # plt.xlabel("Memory Bandwidth (GiB/s)")
    # plt.savefig("plots/perf_gt.png")
    # # plt.savefig("plots/perf_gt.eps", format = "eps")
    # plt.savefig("plots/perf_gt.pdf", format = "pdf")
    # plt.clf()
    
    new_labels = {l:f"{l} ({len(df[df.Label == l])})" for l in df.Label.unique()}
    
    df["Label (# of jobs)"] = df.Label.apply(new_labels.get)
                      
    
    plt.text(2**-30, 2**-18, f"Peak memory bandwidth 1024 GByte/s", rotation = 40)
    plt.text(2**-4, 1.5*top_perf, f"Peak performance 3380 Flops/s", rotation = "horizontal")
    plt.vlines(x=int_point, ymin = 0, ymax = top_perf, color="black", linestyle="dashed")
    plt.text(int_point/4, 2**-21, "Ridge point", rotation = "vertical")
    sns.scatterplot(data = df, x = "arithm_ints", y = "p", hue = "Label (# of jobs)")
    plt.plot(x, mem_line, color="black")
    plt.xscale("log", base=2)
    plt.yscale("log", base=2)
    plt.xlabel("Operational intensity (Flops/Byte)")
    plt.ylabel("Performance (GFlops/s)")
    plt.tight_layout()
    plt.savefig("plots/roofline_gt.png", dpi = 500)
    # plt.savefig("plots/roofline_gt.eps", format = "eps")
    # plt.savefig("plots/roofline_gt.pdf", format = "pdf")
    plt.clf()
    
    new_labels = {freq:f"{freq} ({len(df[df['Frequency (GHz)'] == freq])})" for freq in df["Frequency (GHz)"].unique()}
        
    df["Frequency (GHz) (# of jobs)"] = df["Frequency (GHz)"].apply(new_labels.get)
    
    ax = plt.plot(x, mem_line, color="black")
    l_x, l_y = ax[0].get_data()
    # plt.text(2**-30, 2**-18, f"Peak memory bandwidth", rotation = 41) #{mem_bandwidth} Gib/s
    # plt.text(2**3, 1.5*top_perf, f"Peak performance", rotation = "horizontal") #{top_perf} GFLOP/s
    # plt.vlines(x=int_point, ymin = 0, ymax = top_perf, color="black", linestyle="dashed")
    # plt.text(int_point/4, 2**-21, "Ridge point", rotation = "vertical")
    # sns.scatterplot(data = df, x = "arithm_ints", y = "p", hue = "Frequency (GHz) (# of jobs)", palette=['#FFFFFF', '#FFFFFF'], alpha = 0)
    # plt.text(2**-26, 2**-27, f"Memory bound")
    # plt.text(2**3, 2**-27, f"Compute bound")
    # plt.legend([],[], frameon=False)
    plt.fill_between(l_x, l_y, where = (l_x < int_point), interpolate=True, color = "#1f77b4", alpha=0.35)
    plt.fill_between(l_x, l_y, where = (l_x >= int_point), interpolate=True, color = "#ff7f0e", alpha=0.35)
    # plt.xscale("log", base=2)
    # plt.yscale("log", base=2)
    # plt.xlabel("Operational intensity (GFLOP/GiB)")
    # plt.ylabel("Performance (GFLOP/s)")
    plt.text(2**-30, 2**-18, f"Peak memory bandwidth 1024 GByte/s", rotation = 40)
    plt.text(2**-4, 1.5*top_perf, f"Peak performance 3380 Flops/s", rotation = "horizontal")
    plt.vlines(x=int_point, ymin = 0, ymax = top_perf, color="black", linestyle="dashed")
    plt.text(int_point/4, 2**-21, "Ridge point", rotation = "vertical")
    #sns.scatterplot(data = df, x = "arithm_ints", y = "p", hue = "Label (# of jobs)")
    plt.plot(x, mem_line, color="black")
    plt.xscale("log", base=2)
    plt.yscale("log", base=2)
    plt.xlabel("Operational intensity (Flops/Byte)")
    plt.ylabel("Performance (GFlops/s)")
    plt.tight_layout()
    sns.scatterplot(data = df, x = "arithm_ints", y = "p", hue = "Frequency (GHz) (# of jobs)", palette=['#2ca02c', '#d62728'])
    plt.savefig("plots/roofline_fq.png", dpi = 500)
    # # plt.savefig("plots/roofline_fq.eps", format = "eps"d)
    # # plt.savefig("plots/roofline_fq.pdf", format = "pdf")
    plt.clf()
    
    # sns.histplot(data = df, x = "Frequency (GHz)", hue = "Label", multiple="dodge", stat = "percent")
    # plt.ylabel("% of jobs")
    # # plt.yscale("log")
    # plt.tight_layout()
    # plt.savefig("plots/label_fq.png")
    # # plt.savefig("plots/roofline_fq.eps", format = "eps")
    # plt.savefig("plots/label_fq.pdf", format = "pdf")
    
    # plt.clf()
    
    
def characterize(st:datetime, et:datetime, feature_encoder:IFeatureEncoder = SBEncoder, job_characteriser:IJobCharacterizer = FugakuJobCharacteriser, classification_model:IClassificationModel = KNN, model_weights_path:str = "saved_model", logging_path:str = None) -> bool:
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
        # Service connector
        service_connector = ServiceConnector(service_url)
            
        # Fetching new job data          
        test_data, t, e = service_connector.fetch_data(st=st, et= day, feat = "edt")
        
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
            with open(os.path.join(logging_path, "log.txt"), "a") as f:
                f.write(f"[{str(datetime.now())}] Total Training time: {str(tot_time_train)}, Model Training Time: {str(time_train)}, Total train data: {len(classes)}, Memory-bound: {len(classes[classes == 'memory-bound'])}, Compute-bound: {len(classes[classes == 'compute-bound'])}\n")
        
    except Exception as e:
        if logging_path:
            # Logging of training operation
            with open(os.path.join(logging_path, "log.txt"), "a") as f:
                f.write(f"Error: {e}")
        return False
    else:
        return True
        

            
    
    
    
    
    
    
    