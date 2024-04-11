from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import argparse

from models.containers import Container
from route.classification_model import classification_model_api
from route.characterize import characterize_api
from route.fetch_data import fetch_data_api

def initialise_mcbound() -> Flask:
    
    # App initialization 
    app = Flask("mcbound-framework")
    
    # CORS policy setup
    CORS(app)
            
    container = Container()
                  
    container.wire(packages=["route"])
    
    # Dependency injection
    app.container = container
    
    # Routes registration
    app.register_blueprint(classification_model_api)
    app.register_blueprint(characterize_api)
    app.register_blueprint(fetch_data_api)
    
    return app

if __name__ == "__main__":
        
    # Add parser for the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, required=False, default=8080)
    
    args = parser.parse_args()
        
    mcbound = initialise_mcbound()
 
    mcbound.run(port=args.port)
    
    