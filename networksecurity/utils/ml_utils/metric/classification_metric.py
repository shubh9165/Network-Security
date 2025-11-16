import os
import sys
from sklearn.metrics import precision_score,recall_score,f1_score
from networksecurity.entity.artifacts_entitiy import ClassificationMetricsArtifacts
from networksecurity.exception.exception import CustomException


def get_classification_metrics(y_true,y_pred)->ClassificationMetricsArtifacts:
    
    try:
        model_f1_score=f1_score(y_true,y_pred)
        model_precision_score=precision_score(y_true,y_pred)
        model_recall_score=recall_score(y_true,y_pred)

        Classification_Metrics_Artifacts=ClassificationMetricsArtifacts(
            f1_score=model_f1_score,
            precision_score=model_precision_score,
            recall_score=model_recall_score

        )
        return Classification_Metrics_Artifacts
    except Exception as e:
        raise CustomException(e,sys)