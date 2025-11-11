from setuptools import find_packages,setup
from typing import List

HYPHENDOTE='-e .'
def get_requirments()->List[str]:

    requirments_list:List[str]=[]

    try:
        with open('requirment.txt','r') as file:

            lines=file.readlines()

            for line in lines:
                requirment=line.strip()

                if  requirment and requirment!=HYPHENDOTE:
                    requirments_list.append(requirment)
    
            return requirments_list
    except :
        print("requirment file not found")

setup(
    name='Network Security',
    author="shubh patel",
    author_email="shubhpatel915@gmail.com",
    packages=find_packages(),
    requires=get_requirments()
)