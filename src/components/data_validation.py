import json
import sys
import os

import pandas as pd
# from evidently.model_profile import Profile
# from evidently.model_profile.sections import DataDriftProfileSection
from pandas import DataFrame

from src.constant.training_pipeline import SCHEMA_FILE_PATH
from src.entity.artifact import DataIngestionArtifact, DataValidationArtifact
from src.entity.config import DataValidationConfig
from src.exception import SensorException
from src.logger import logging
from scipy.stats import ks_2samp
from src.utils.main_utils import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            logging.error(e)
            raise SensorException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            return number_of_columns == len(dataframe.columns)
        except Exception as e:
            logging.error(e)
            raise SensorException(e, sys)

    def is_numerical_column_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            dataframe_columns = dataframe.columns
            status = True
            missing_numerical_columns = []
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    status = False
                    missing_numerical_columns.append(column)
            logging.info(
                f"Missing numerical column: {missing_numerical_columns}")
            return status

        except Exception as e:
            logging.error(e)
            raise SensorException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            report = {}
            status = True
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_distribution = ks_2samp(d1, d2)
                is_found = is_same_distribution.pvalue <= threshold
                status = not is_found
                report[column] = {
                    "p_value": float(is_same_distribution.pvalue),
                    "drift_status": is_found,
                }
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
            return status
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        # sourcery skip: raise-specific-error
        try:
            validate_error_msg = ""
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            # Reading data from test files and training files locations
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            # Validate number_of_columns the training and testing data frames
            if not self.validate_number_of_columns(dataframe=train_dataframe):
                validate_error_msg = f"{validate_error_msg} Number of columns in the train data frame is not equal to the number of columns in the schema file"
            if not self.validate_number_of_columns(dataframe=test_dataframe):
                validate_error_msg = f"{validate_error_msg} Number of columns in the test data frame is not equal to the number of columns in the schema file"
            # Validate is_numerical_column_exist the training and testing data frames
            if not self.is_numerical_column_exist(dataframe=train_dataframe):
                validate_error_msg = f"{validate_error_msg} Missing numerical columns in the train data frame"
            if not self.is_numerical_column_exist(dataframe=test_dataframe):
                validate_error_msg = f"{validate_error_msg} Missing numerical columns in the test data frame"
            if validate_error_msg != "":
                raise Exception(validate_error_msg)
            # Detecting dataset drift
            validation_status = self.detect_dataset_drift(
                base_df=train_dataframe, current_df=test_dataframe)
            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
        except Exception as e:
            logging.error(e)
            raise SensorException(e, sys)
