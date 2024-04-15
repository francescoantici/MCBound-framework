from datetime import datetime, timedelta
import os

from utils.log_utils import write_log

def inference(job_data:list, logging_path:str = None) -> list:
    """_summary_

    Args:
        job_data (list): List containing the job data.
        logging_path (str): Path to save logs.
    Returns:
        List of the predictions for the jobs data fetched.
    """
    try:        
        # Perform predictions
        pred_class, i_t, e = service_connector.predict(job_data)
        
        if e:
            raise Exception(e)
        
        if logging_path:
            # Logging
            write_log(os.path.join(logging_path, "log"), f"Total inference time: {i_t}, Average inference time per job {float(i_t)/len(test_data)}, Number of Jobs: {len(test_data)}\n")
    except Exception as e:
        if logging_path:
            # Logging
            write_log(os.path.join(logging_path, "log"), f"Error: {e}\n")
        return []
    else:
        return pred_class
        
             
    
    

            
        
            
        
        
    
    
    
    
    