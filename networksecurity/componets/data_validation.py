from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.constant import training_pipeline
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifacts_entitiy import DataValidationArtifacts,DataIngestionArtifacts
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
import sys
import pandas as pd
from scipy.stats import ks_2samp
import os

class DataValidation:
    def __init__(self,data_validation_config=DataValidationConfig
                 ,data_ingestion_artifacts=DataIngestionArtifacts):
        
        try:
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifacts=data_ingestion_artifacts
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e,sys)
        
    @staticmethod
    def read_dataframe(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)
    
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self._schema_config)
            logging.info(f"Required Number of Columns{number_of_columns}")
            logging.info(f"Data freame has {len(dataframe.columns)}")

            if number_of_columns==len(dataframe.columns):
                return True
            return False
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def check_numeric_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_feature=dataframe.select_dtypes(exclude='object').columns
            if len(numerical_feature)>0:
                return True
            return False
        
        except Exception as e:
            raise CustomException(e,sys)
    
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:

        try:
            report={}
            status=True

            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)

                if threshold<=is_same_dist.pvalue:
                    is_founded=False
                else:
                    is_founded=True
                    status=False
                report.update({column:{
                    'pvalue':float(is_same_dist.pvalue),
                    'drift_status':is_founded
                }})
                
            drift_report_file_path=self.data_validation_config.drift_report_file_path

            dir_name=os.path.dirname(drift_report_file_path)

            os.makedirs(dir_name,exist_ok=True)

            write_yaml_file(file_path=drift_report_file_path,content=report)

            return status
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_validation(self):

        try:
            train_file_path=self.data_ingestion_artifacts.trained_file_path
            test_file_path=self.data_ingestion_artifacts.tested_file_path

            train_df=DataValidation.read_dataframe(file_path=train_file_path)
            test_df=DataValidation.read_dataframe(file_path=test_file_path)

            status=self.validate_number_of_columns(train_df)
            if not status:
                error_message=f"Train data does not contains all the columns"

            status=self.validate_number_of_columns(test_df)

            if not status:
                error_message=f"Test data does not contains all the columns"
            
            status=self.check_numeric_columns(train_df)

            if not status:
                error_message=f"Train data does not contain numerical columns"
            
            status=self.check_numeric_columns(test_df)

            if not status:
                error_message=f"test data does not contain numerical columns"
            
            status=self.detect_dataset_drift(base_df=train_df,current_df=test_df)

            dir_name=os.path.dirname(self.data_validation_config.valid_train_file_path)

            os.makedirs(dir_name,exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)

            dir_name=os.path.dirname(self.data_validation_config.valid_test_file_path)

            os.makedirs(dir_name,exist_ok=True)

            test_df.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)

            data_validation_artifact = DataValidationArtifacts(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifacts.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifacts.tested_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)
