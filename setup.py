from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
  '''
  Parse requirements.txt file and return a list of requirements.
  '''
  requirement_lst: List[str] = []
  try:
    with open('requirements.txt', 'r') as f:
      lines = f.readlines()

      # Process each line to remove comments and whitespace
      for line in lines:
        requirement= line.strip() # Ignore whitespaces 
        if (requirement and requirement != '-e .' ): # Ignore empty lines and '-e.' lines
          requirement_lst.append(requirement) # Append to the requirement list

          
  except FileNotFoundError:
    print('requirements.txt file not found.')
  
  return requirement_lst

setup(
  name="NewsSentimentAnalysis",
  version="0.0.1",
  author="Ayush",
  author_email="ayushjaswal4543@gmail.com",
  packages=find_packages(),
  install_requires=get_requirements() 
)