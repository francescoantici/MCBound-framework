from dependency_injector import containers, providers
import os

from service.job_characterizer.fugaku_job_characterizer import FugakuJobCharacterizer
from service.data_fetcher.parquet_data_fetcher import ParquetDataFetcher
from service.classification_model.knn import KNN
from service.feature_encoder.sb_feature_encoder import SBEncoder



class Container(containers.DeclarativeContainer):
    
    config = providers.Configuration(json_files=["config/config.json"])
    
    # Data fetcher 
    data_fetcher = providers.Singleton(ParquetDataFetcher, config.data_file) 
    
    # Prediction model for the jobs
    classification_model = providers.Singleton(KNN.from_saved_model, config.model_weights_path) 
            
    # Job characterizer 
    job_characterizer = providers.Singleton(FugakuJobCharacterizer)
    
    # Feature encoder 
    feature_encoder = providers.Singleton(SBEncoder)