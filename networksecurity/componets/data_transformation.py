import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.entity.artifacts_entitiy import DataTransformationArtifacts,DataValidationArtifacts
from networksecurity.entity.config_entity import DataTransformationConfig,DataValidationConfig
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTE_PRAMS,TARGET_COLUMN
from networksecurity.utils.main_utils.utils import save_numpy_arr_data,save_object



class DataTransformation:
    def __init__(self,data_validation_artifacts:DataValidationArtifacts,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifats:DataValidationArtifacts=data_validation_artifacts
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise CustomException(e,sys)
    
    @staticmethod
    def read_dataframe(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)
        


    def get_data_transformer(cls)->Pipeline:
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTE_PRAMS)
            processor:Pipeline=Pipeline([('imputer',imputer)])
            return processor
        except Exception as e:
            raise CustomException(e,sys)
        


    def initiate_data_transformation(self)->DataTransformationArtifacts:

        try:
            logging.info("Enterd into intiate data transformation folder ")
            train_df=DataTransformation.read_dataframe(self.data_validation_artifats.valid_train_file_path)
            test_df=DataTransformation.read_dataframe(self.data_validation_artifats.valid_test_file_path)


            #dividing into independent and dependent features
            input_feature_train_df=train_df.drop([TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)

            input_feature_test_df=test_df.drop([TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)

            preprocessor=self.get_data_transformer()

            trasformed_train_input_feature=preprocessor.fit_transform(input_feature_train_df)
            transformed_test_input_feature=preprocessor.transform(input_feature_test_df)

            train_arr=np.c_[trasformed_train_input_feature,np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_test_input_feature,np.array(target_feature_test_df)]


            save_numpy_arr_data(self.data_transformation_config.data_transformed_train_file_path,train_arr)
            save_numpy_arr_data(self.data_transformation_config.data_transformed_test_file_path,test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor)

            Data_Transformation_Artifacts=DataTransformationArtifacts(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.data_transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.data_transformed_test_file_path
            )

            return Data_Transformation_Artifacts
            

            
        except Exception as e:
            raise CustomException(e,sys)

       
