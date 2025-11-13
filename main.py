from networksecurity.componets.data_ingestion import DataIngestion
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
import sys



if __name__=='__main__':
    try:
         TrainingPipelineConfig=TrainingPipelineConfig()
         DataIngestionConfig=DataIngestionConfig(TrainingPipelineConfig)
         DataIngestion=DataIngestion(DataIngestionConfig)
         dataIngestionArtifacts=DataIngestion.initiate_data_ingestion()
         logging.info("done")
         print(dataIngestionArtifacts)

    except Exception as e:
        raise CustomException(e,sys)

