from dependency_injector import containers, providers
import os

from service.job_characterizer.fugaku_job_characterizer import FugakuJobCharacterizer
from service.data_fetcher.fugaku_data_fetcher import FugakuDataFetcher
from service.classification_model.knn import KNN
from service.feature_encoder.sb_feature_encoder import SBEncoder

class Container(containers.DeclarativeContainer):
    
    # Configuration from json file
    config = providers.Configuration(json_files=["config/config.json"])
    
    # Data fetcher singleton instance creation
    data_fetcher = providers.Singleton(FugakuDataFetcher) 
    
    # Prediction model singleton instance creation
    classification_model = providers.Singleton(KNN.from_saved_model, config.model_weights_path) 
            
    # Job characterizer singleton instance creation
    job_characterizer = providers.Singleton(FugakuJobCharacterizer)
    
    # Feature encoder singleton instance creation
    feature_encoder = providers.Singleton(SBEncoder)