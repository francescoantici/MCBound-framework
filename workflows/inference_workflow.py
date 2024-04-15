from datetime import datetime, timedelta
import os

from utils.service_connector import ServiceConnector

def inference(service_url:str, st:datetime, et:datetime, logging_path:str = None) -> list:
    """_summary_

    Args:
        service_url (str): Url of the MCBound instance.
        st (datetime): Start time to fetch jobs.
        et (datetime): End time to fetch jobs.
        logging_path (str): Path to save logs
    Returns:
        List of the predictions for the jobs data fetched.
    """
    try:
        # Service connector
        service_connector = ServiceConnector(service_url)
            
        # Fetching new job data          
        test_data, t, e_d = service_connector.fetch_data(st=st, et= day, feat = "adt")
        
        if e_d:
            raise Exception(e_d)
        
        # Perform predictions
        pred_class, i_t, e = service_connector.predict(job_data)
        
        if e:
            raise Exception(e)
        
        if logging_path:
            # Logging
            with open(os.path.join(args.output, f"results_{str(et.date())}.txt"), "w") as f:
                f.write(f"Total inference time: {i_t}, Average inference time per job {float(i_t)/len(test_data)}, Number of Jobs: {len(test_data)}\n")
    except Exception as e:
        if logging_path:
            # Logging
            with open(os.path.join(args.output, f"results_{str(et.date())}.txt"), "w") as f:
                f.write(f"Error: {e}\n")
        return []
    else:
        return pred_class
        
             
    
    

            
        
            
        
        
    
    
    
    
    