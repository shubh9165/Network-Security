from networksecurity.componets.data_ingestion import DataIngestion
from networksecurity.componets.data_validation import DataValidation
from networksecurity.componets.data_transformation import DataTransformation
from networksecurity.componets.model_trainer import ModelTrainer



from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
import sys



if __name__=='__main__':
    try:
         TrainingPipelineConfig=TrainingPipelineConfig()
         DataIngestionConfig=DataIngestionConfig(TrainingPipelineConfig)
         DataIngestion=DataIngestion(DataIngestionConfig)
         dataIngestionArtifacts=DataIngestion.initiate_data_ingestion()
         print(dataIngestionArtifacts)
         logging.info("Data ingestion process done")

         DataValidationConfig=DataValidationConfig(TrainingPipelineConfig)
         DataValidation=DataValidation(DataValidationConfig,dataIngestionArtifacts)
         data_validation_artifacts=DataValidation.initiate_data_validation()
         logging.info("Data validation process done")
         print(data_validation_artifacts)

         DataTransformationConfig=DataTransformationConfig(TrainingPipelineConfig)
         DataTransformation=DataTransformation(data_validation_artifacts,DataTransformationConfig)
         data_transformation_artifacts=DataTransformation.initiate_data_transformation()
         print(data_transformation_artifacts)
         logging.info("Data transformation process done")

         ModelTrainerConfig=ModelTrainerConfig(TrainingPipelineConfig)
         model_trainer=ModelTrainer(data_transformation_artifacts,ModelTrainerConfig)
         model_trainer_artifacts=model_trainer.initatiate_model_trainer()
         print(model_trainer_artifacts)
         logging.info("Model training process doen")



    except Exception as e:
        raise CustomException(e,sys)

