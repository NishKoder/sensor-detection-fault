import sys
from src.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME
import os
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from src.exception import SensorException
from src.logger import logging


class TargetValueMapping:
    def __init__(self):
        self.neg: int = 0
        self.pos: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))

class SensorModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: DataFrame) -> DataFrame:
        logging.info("Entered predict method of SensorTruckModel class")
        try:
            logging.info("Using the trained model to get predictions")
            transformed_feature = self.preprocessing_object.transform(dataframe)
            logging.info("Used the trained model to get predictions")
            return self.trained_model_object.predict(transformed_feature) # type: ignore
        except Exception as e:
            raise SensorException(e, sys) # type: ignore

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"
    

class ModelResolver:
    def __init__(self, model_dir = SAVED_MODEL_DIR):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise e
        
    def get_best_model_path(self) -> str:
        try:
            timestamps = list(os.listdir(SAVED_MODEL_DIR))
            latest_timestamp = max(timestamps)
            return os.path.join(self.model_dir, f"{latest_timestamp}", MODEL_FILE_NAME)
        except Exception as e:
            raise e
        
    
    def is_model_exists(self) -> bool:
        try:
            if not os.path.exists(self.model_dir):
                return False
            timestamps = os.listdir(self.model_dir)
            if len(timestamps) == 0:
                return False
            latest_model_path = self.get_best_model_path()
            return bool(os.path.exists(latest_model_path))
        except Exception as e:
            raise e