import sys
import os
import pandas as pd
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
import pymongo
from dotenv import load_dotenv
import numpy as np
from sklearn.model_selection import train_test_split
from networksecurity.entity.artifacts_entitiy import DataIngestionArtifacts

load_dotenv()

MONOGO_DB_URL=os.getenv('MONGO_DB_URL')


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config   
        except Exception as e:
            raise CustomException(e,sys)


    def export_data_from_mongodb(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_clint=pymongo.MongoClient(MONOGO_DB_URL)
            collection=self.mongo_clint[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))

            if "_id" in df.columns:
                df.drop(['_id'],axis=1,inplace=True)

            df.replace({"na":np.nan},inplace=True)
            return df
        
        except Exception as e:
            raise CustomException(e,sys)
    


    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,header=True,index=False)
            return dataframe
        except Exception as e:
            raise CustomException(e,sys)


    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            logging.info('now we spliting data into train and test')
            train_set,test_set=train_test_split(dataframe,
                                                test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Successfully splited")
            train_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            test_path=os.path.dirname(self.data_ingestion_config.testing_file_path)


            os.makedirs(train_path,exist_ok=True)
            os.makedirs(test_path,exist_ok=True)


            train_set.to_csv(self.data_ingestion_config.training_file_path,header=True,index=False)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logging.info("exported train and test data ")


        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_ingestion(self):
        try:
            logging.info("we initiating data ingestion ")
            dataframe=self.export_data_from_mongodb()
            logging.info("mongodb readed ")
            dataframe=self.export_data_into_feature_store(dataframe)
            logging.info("data exported from mongodb ")
            self.split_data_as_train_test(dataframe=dataframe)
            dataIngestionArtifacts=DataIngestionArtifacts(trained_file_path=self.data_ingestion_config.training_file_path,tested_file_path=self.data_ingestion_config.testing_file_path)
            return dataIngestionArtifacts

        except Exception as e:
            raise CustomException(e,sys)
