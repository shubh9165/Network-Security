import sys
import os
import numpy as np
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifacts_entitiy import DataTransformationArtifacts,ModelTrainerArtifacts
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.main_utils.utils import load_numpy_arr_data,load_object,evaluate_model,save_object
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_metrics
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression



class ModelTrainer:
    def __init__(self,data_transformation_artifacts:DataTransformationArtifacts
                 ,model_trainer_config:ModelTrainerConfig):
        try:
           self.data_transformationartifacts=data_transformation_artifacts
           self.model_trainerconfig=model_trainer_config

        except Exception as e:
            raise CustomException(e,sys)
    

    def train_model(self,x_train,x_test,y_train,y_test)->ModelTrainerArtifacts:

        try:

            models={
                "Random Forest":RandomForestClassifier(verbose=1),
                "Decison Tree":DecisionTreeClassifier(),
                "Gradient Boosting":GradientBoostingClassifier(verbose=1),
                "Logistic Regresion":LogisticRegression(verbose=1),
                "AdaBoost":AdaBoostClassifier()
            }
            params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            

        }
            
            model_report:dict=evaluate_model(X_train=x_train,y_train=y_train,X_test=x_test,y_test=y_test,models=models,param=params)

            best_model_scor=max(sorted(model_report.values()))

            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_scor)
            ]

            best_model=models[best_model_name]

            y_train_pred=best_model.predict(x_train)

            classification_train_metrics=get_classification_metrics(y_true=y_train,y_pred=y_train_pred)

            y_test_pred=best_model.predict(x_test)

            classification_test_metrics=get_classification_metrics(y_true=y_test,y_pred=y_test_pred)

            preprocessor=load_object(self.data_transformationartifacts.transformed_object_file_path)

            dir_name=os.path.dirname(self.model_trainerconfig.trained_model_file_path)
            
            os.makedirs(dir_name,exist_ok=True)

            network_model=NetworkModel(preprocessor=preprocessor,model=best_model)

            save_object(self.model_trainerconfig.trained_model_file_path,obj=network_model)

            model_trainer_artifacts=ModelTrainerArtifacts(trained_model_file_path=self.model_trainerconfig.trained_model_file_path,
                                  train_metrics_artifacts=classification_train_metrics,test_metrics_artifacts=classification_test_metrics)
            
            logging.info(f"model Trainer artifact {model_trainer_artifacts}")

            return model_trainer_artifacts
        
        except Exception as e:
            raise CustomException(e,sys)
        


    def initatiate_model_trainer(self)->ModelTrainerArtifacts:
        try:
            train_file_path=self.data_transformationartifacts.transformed_train_file_path
            test_file_path=self.data_transformationartifacts.transformed_test_file_path

            train_arr=load_numpy_arr_data(train_file_path)
            test_arr=load_numpy_arr_data(test_file_path)

            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            return self.train_model(x_train=x_train,x_test=x_test,y_test=y_test,y_train=y_train)
            

        except Exception as e:
            raise CustomException(e,sys)
