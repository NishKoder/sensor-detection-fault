from src.pipeline.training_pipeline import TrainingPipeline
from src.exception import SensorException
from src.logger import logging
from src.utils.main_utils import read_yaml_file
from src.constant.application import APP_HOST, APP_PORT
from src.constant.training_pipeline import SAVED_MODEL_DIR
from src.ml.model.estimator import ModelResolver, TargetValueMapping
from src.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware

import os
import sys
from fastapi import FastAPI, File, UploadFile
from uvicorn import run as app_run
from fastapi.responses import Response, RedirectResponse
import pandas as pd

env_file_path = "/config/workspace/env.yaml"


def set_env_variable(env_file_path):
    env_config = read_yaml_file(env_file_path)
    os.environ["MONGO_DB_URL"] = env_config["MONGO_DB_URL"]
    
    
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
    )


@app.get("/", tags = ["authentication"])
async def index():
    return RedirectResponse(url = "/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training Pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!!")
    except Exception as e:
        return Response(f"Error Occured! {e}")
    


@app.get("/predict")
async def predict_route(request, file : UploadFile = File(...)):
    try:
        #get data from user csv file
        #conver csv file to dataframe
        df = pd.read_csv(file.file)
        print(df.tail(10))
        model_resolver = ModelResolver(model_dir = SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path = best_model_path)
        y_pred = model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(), 
                                       inplace=True)
        return df.to_html()
        #decide how to return file to user.
        
    except Exception as e:
        raise Response(f"Error Occured! {e}")
    
    
    
def main():
    try:
        #set_env_variable(env_file_path)
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
    except Exception as e:
        logging.exception(e)



if __name__ == '__main__':
    #set_env_variable(env_file_path)
    app_run(app, host = APP_HOST, port = APP_PORT)
    #main()