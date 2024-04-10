from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import argparse

from models.containers import Container
import route 
from route.classification_model import classification_model_api
from route.characterise import characterise_api
from route.fetch_data import fetch_data_api

def initialise_mcbound() -> Flask:
    container = Container()

    # App initialization 
    app = Flask("mcbound-framework")
    
    # CORS policy setup
    CORS(app)
        
    container.config.feature_encoder.weights.from_env(os.environ["FEATURE_ENCODER_WEIGHTS"])
    container.config.classification_model.model_weights.from_env(os.environ["MODEL_WEIGHTS_PATH"])
    container.config.data_fetcher.parquet_file.from_env(os.environ["PARQUET_FILE"])
    
    container.wire(modules=[route])
    
    # Dependency injection
    app.container = container
    
    # Routes registration
    app.register_blueprint(classification_model_api)
    app.register_blueprint(characterise_api)
    app.register_blueprint(fetch_data_api)
    
    return app

if __name__ == "__main__":
        
    # Add parser for the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", type=str, required=False, default=None)
    
    args = parser.parse_args()
    
    # Load variables for the models 
    load_dotenv(args.env)
    
    mcbound = initialise_mcbound()
                    
    mcbound.run(port=os.environ["SERVICE_PORT"])
    