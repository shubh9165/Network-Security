from dataclasses import dataclass


#This is use as a output in data ingestion 
@dataclass
class DataIngestionArtifacts:
    trained_file_path:str
    tested_file_path:str

#it is use as a output in data validation and input in data transformation
@dataclass
class DataValidationArtifacts:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str


# this is use as a output in data transformation and input as a model trainer
@dataclass
class DataTransformationArtifacts:
    transformed_object_file_path:str
    transformed_train_file_path:str
    transformed_test_file_path:str