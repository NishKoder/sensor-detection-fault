from src.entity.config import TrainingPipelineConfig, DataIngestionConfig
from src.exception import SensorException
from src.logger import logging
from src.entity.artifact import DataIngestionArtifact
import sys
from src.components.data_ingestion import DataIngestion


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Data ingestion started")
            self.data_ingestion_config = DataIngestionConfig(
            training_pipeline_config=self.training_pipeline_config)
            data_ingestion:DataIngestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed successfully and artifact: %s", data_ingestion_artifact)
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)  # type: ignore

    def start_data_validation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)  # type: ignore
        logging.info("Data validation started")

    def start_data_transformation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)  # type: ignore
        logging.info("Data transformation started")

    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)  # type: ignore
        logging.info("Model trainer started")

    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)  # type: ignore
        logging.info("Model evaluation started")

    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)  # type: ignore
        logging.info("Model pusher started")

    def run_pipeline(self):
        try:
            logging.info("Pipeline started")
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            logging.info("Pipeline completed successfully")
        except Exception as e:
            raise SensorException(e, sys)  # type: ignore
