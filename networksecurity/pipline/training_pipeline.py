import os
import sys

from networksecurity.componets.data_ingestion import DataIngestion
from networksecurity.componets.data_validation import DataValidation
from networksecurity.componets.data_transformation import DataTransformation
from networksecurity.componets.model_trainer import ModelTrainer

from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging


from networksecurity.entity.config_entity import (
    DataIngestionConfig,DataTransformationConfig,DataValidationConfig,ModelTrainerConfig,TrainingPipelineConfig
)

from networksecurity.entity.artifacts_entitiy import (
    DataIngestionArtifacts,DataValidationArtifacts,DataTransformationArtifacts,ModelTrainerArtifacts
)


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Data Ingestion process start")
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifacts=data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion process done and data ingestion artifact {data_ingestion_artifacts}")
            return data_ingestion_artifacts
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifacts:DataIngestionArtifacts):

        try:
            self.data_validation_config=DataValidationConfig(training_pipeline_config=TrainingPipelineConfig)
            logging.info("Data Validation process start")
            data_validation=DataValidation(data_ingestion_artifacts=data_ingestion_artifacts,data_validation_config=self.data_validation_config)
            data_validation_artifacts=data_validation.initiate_data_validation()
            logging.info(f"Data Validation Process done and data validation artifact {data_validation_artifacts}")
            return data_validation_artifacts
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_transformation(self,data_validation_artifacts:DataValidationArtifacts):


        try:
            self.data_transformation_config=DataTransformationConfig(training_pipeline_config=TrainingPipelineConfig)
            logging.info(f"Data Transformation process start")
            data_transformation=DataTransformation(data_validation_artifacts=data_validation_artifacts,data_transformation_config=self.data_transformation_config)
            data_transformation_artifacts=data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation process done and data transformation artifacts {data_transformation_artifacts}")
            return data_transformation_artifacts
        
        except Exception as e:
            raise CustomException(e,sys)
        
    
    def start_model_trainer(self,data_transformation_artifacts:DataTransformationArtifacts)->ModelTrainerArtifacts:

        try:
            self.model_trainer_config=ModelTrainerConfig(training_pipeline_config=TrainingPipelineConfig)
            logging.info("Model training process start")
            model_trainer=ModelTrainer(data_transformation_artifacts=data_transformation_artifacts,model_trainer_config=self.model_trainer_config)
            model_trainer_artifacts=model_trainer.initatiate_model_trainer()
            logging.info(f"Model trainer process done and model trainer artifacts {model_trainer_artifacts}")
            return model_trainer_artifacts
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def run_pipeline(self):

        try:

            data_ingestion_artifacts=self.start_data_ingestion()
            data_validation_artifacts=self.start_data_validation(data_ingestion_artifacts=data_ingestion_artifacts)
            data_transformation_artifacts=self.start_data_transformation(data_validation_artifacts=data_ingestion_artifacts)
            model_trainer_artifacts=self.start_model_trainer(data_transformation_artifacts=data_transformation_artifacts)
            return model_trainer_artifacts

        except Exception as e:
            raise CustomException(e,sys)