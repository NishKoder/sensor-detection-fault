from src.configuration.mongodb_connection import MongoDatabaseClient
from src.exception import SensorException
from src.logger import logging
import sys
from src.entity.config import TrainingPipelineConfig,DataIngestionConfig
from src.pipeline.training_pipeline import TrainingPipeline

# Test Exceptions
def test_exception():
    try:
        logging.info("Test exception")
        x=1/0
    except Exception as e:
        raise SensorException(e,sys) # type: ignore
if __name__ == '__main__':
    # mongo_db_client = MongoDatabaseClient()
    # print(mongo_db_client.database.list_collection_names()) # type: ignore
    # try:
    #     test_exception()
    # except Exception as e:
    #     print(e)
    # training_pipeline_config=TrainingPipelineConfig()
    # data_ingestion_config=DataIngestionConfig(training_pipeline_config)
    # print(data_ingestion_config.__dict__)
    training_pipeline=TrainingPipeline()
    training_pipeline.run_pipeline()
