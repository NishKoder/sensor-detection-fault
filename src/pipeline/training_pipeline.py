from src.entity.config import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from src.exception import SensorException
from src.logger import logging
from src.entity.artifact import DataIngestionArtifact, DataValidationArtifact
import sys
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Data ingestion started")
            self.data_ingestion_config = DataIngestionConfig(
                training_pipeline_config=self.training_pipeline_config)
            data_ingestion: DataIngestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(
                "Data ingestion completed successfully and artifact: %s", data_ingestion_artifact)
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)  # type: ignore

    def start_data_validation(
        self, data_ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
        logging.info(
            "Entered the start_data_validation method of TrainPipeline class")
        try:
            self.data_validation_config = DataValidationConfig(
                training_pipeline_config=self.training_pipeline_config)
            data_validation: DataValidation = DataValidation(
                data_validation_config=self.data_validation_config,
                data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(
                "Data validation completed successfully and artifact: %s", data_validation_artifact)
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)
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
            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact: DataValidationArtifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact)
            logging.info("Pipeline completed successfully")
        except Exception as e:
            raise SensorException(e, sys)  # type: ignore
