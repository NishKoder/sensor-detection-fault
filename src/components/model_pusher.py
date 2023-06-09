from src.utils.main_utils import(
    load_numpy_array_data, save_object, 
    load_object, write_yaml_file
    )

from src.exception import SensorException
from src.logger import logging

from src.entity.artifact import(
                    ModelPusherArtifact, 
                    ModelEvaluationArtifact)

from src.entity.config import ModelPusherConfig
import os,sys
import shutil



class ModelPusher:
    def __init__(self, 
                 model_eval_artifact : ModelEvaluationArtifact,
                 model_pusher_config : ModelPusherConfig):
     
        try:
            self.model_eval_artifact = model_eval_artifact
            self.model_pusher_config = model_pusher_config
        except Exception as e:
            SensorException(e, sys)
            
        
    def initiate_model_pusher(self) -> ModelPusherArtifact: # type: ignore
        try:
            trained_model_path = self.model_eval_artifact.trained_model_path
            
            # Creating model pusher dir to save model
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path), exist_ok = True)
            shutil.copy(src = trained_model_path, dst = model_file_path)
            
            # save model dir
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path), exist_ok = True)
            shutil.copy(src = trained_model_path, dst = saved_model_path)
            
            # prepare artifact
            model_pusher_artifact = ModelPusherArtifact(
                saved_model_path = saved_model_path,
                model_file_path = model_file_path
                )
            
            logging.info(f"Model Pusher Artifact {model_pusher_artifact}")
            return model_pusher_artifact
            
        except Exception as e:
            SensorException(e, sys)