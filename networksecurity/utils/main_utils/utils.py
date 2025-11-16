from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
import sys
import yaml
import pickle
import numpy as np
import os
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

#This is used for read yaml file
def read_yaml_file(file_path)->dict:

    try:
         with open(file_path,'r') as file_obj:
            return yaml.safe_load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    
#this is used for write in yaml file
def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:

    try:
        with open(file_path,'w') as file_obj:
             yaml.dump(content,file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    
#we saving the numpy arr inside of data_transformation file
def save_numpy_arr_data(file_path:str,arr:np.array):

    try:
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,arr)
    except Exception as e:
        raise CustomException(e,sys)
    
#for saving the models or object which we will create 
def save_object(file_path:str,obj:object):
    try:
        logging.info("Entered save_object fuction of mainutils folder ")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("exiting from the save_object fuction of mainUtils folder ")
        
    except Exception as e:
        raise CustomException(e,sys)
    
def load_object(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file{file_path} not exist")
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)

                    
    except Exception as e:
        raise CustomException(e,sys)
    


def load_numpy_arr_data(file_path:str)->np.array:
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    

def evaluate_model(X_train,y_train,X_test,y_test,models,param):

    try:
        report={}

        for i in range(len(list(models))):

            model=list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs=GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            y_train_pred=model.predict(X_train)

            y_test_pred=model.predict(X_test)

            train_model_r2_score=r2_score(y_train,y_train_pred)

            test_model_r2_score=r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]]=test_model_r2_score

            return report
        
    except Exception as e:
        raise CustomException(e,sys)

