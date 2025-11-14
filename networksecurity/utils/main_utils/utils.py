from networksecurity.exception.exception import CustomException
import sys
import yaml

def read_yaml_file(file_path)->dict:

    try:
         with open(file_path,'r') as file_obj:
            return yaml.safe_load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    
def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:

    try:
        with open(file_path,'w') as file_obj:
             yaml.dump(content,file_obj)
    except Exception as e:
        raise CustomException(e,sys)