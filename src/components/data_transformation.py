import sys

import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

from src.constant.training_pipeline import TARGET_COLUMN
from src.entity.artifact import (
    DataTransformationArtifact,
    DataValidationArtifact,
)
from src.entity.config import DataTransformationConfig
from src.exception import SensorException
from src.logger import logging
from src.ml.model.estimator import TargetValueMapping
from src.utils.main_utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig,):
        """
        :param data_validation_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise SensorException(e, sys) # type: ignore

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys) # type: ignore

    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        """
        :return: Pipeline object to transform dataset
        """
        logging.info("Entered get_data_transformer_object method of DataTransformation class")
        try:
            logging.info("Got numerical cols from schema config")
            robust_scaler = RobustScaler()
            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)
            logging.info("Initialized RobustScaler, Simple Imputer")
            preprocessor = Pipeline(steps=[("Imputer", simple_imputer),("RobustScaler", robust_scaler)])
            logging.info("Created preprocessor object from ColumnTransformer")
            logging.info("Exited get_data_transformer_object method of DataTransformation class")
            return preprocessor
        except Exception as e:
            raise SensorException(e, sys) # type: ignore

    def initiate_data_transformation(self,) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")
            preprocessor = self.get_data_transformer_object()
            logging.info("Got the preprocessor object")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(file_path=self.data_validation_artifact.valid_test_file_path)
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(TargetValueMapping().to_dict())
            logging.info("Got train features and test features of Training dataset")
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict())
            
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)
            
            logging.info("Applying SMOTETomek on Training dataset")
            smt = SMOTETomek(sampling_strategy="minority")
            input_feature_train_final, target_feature_train_final = smt.fit_resample(transformed_input_train_feature, target_feature_train_df) # type: ignore
            logging.info("Applied SMOTETomek on training dataset")
            logging.info("Applying SMOTETomek on testing dataset")
            input_feature_test_final, target_feature_test_final = smt.fit_resample(transformed_input_test_feature, target_feature_test_df) # type: ignore
            logging.info("Applied SMOTETomek on testing dataset")
            logging.info("Created train array and test array")
            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr,)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object,)
            logging.info("Saved the preprocessor object")
            logging.info("Exited initiate_data_transformation method of Data_Transformation class")
            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )
        except Exception as e:
            raise SensorException(e, sys) # type: ignore
