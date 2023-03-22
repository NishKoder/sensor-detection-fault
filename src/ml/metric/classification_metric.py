from src.entity.artifact import ClassificationMetricArtifact
from src.exception import SensorException
from src.logger import logging
import os
import sys
from sklearn.metrics import f1_score, precision_score, recall_score


def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score = precision_score(y_true, y_pred)

        return ClassificationMetricArtifact(
            f1_score=model_f1_score, # type: ignore
            precision_score=model_precision_score,# type: ignore
            recall_score=model_recall_score# type: ignore
        )

    except Exception as e:
        raise SensorException(e, sys)
