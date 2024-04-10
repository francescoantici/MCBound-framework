from dependency_injector import containers, providers
import os

from service.job_characteriser.fugaku_job_characteriser import FugakuJobCharacteriser
from service.data_fetcher.parquet_data_fetcher import ParquetDataFetcher
from service.classification_model.knn import KNN
from service.feature_encoder.sb_feature_encoder import SBEncoder

class Container(containers.DeclarativeContainer):
    
    config = providers.Configuration()
    
    # Data fetcher 
    data_fetcher = providers.Singleton(ParquetDataFetcher, config.data_fetcher.parquet_file) 
    
    # Prediction model for the jobs
    classification_model = providers.Singleton(KNN.from_saved_model, config.classification_model.model_weights)
    
    # Job characteriser 
    job_characteriser = providers.Singleton(FugakuJobCharacteriser) 
    
    # Feature encoder 
    feature_encoder = providers.Singleton(SBEncoder, weights = config.feature_encoder.weights)