## Dictionary Service

#### The goal - develop a REST service for retrieving all possible matches of a prefix in a dictionary

#### Endpoints:

- /dictionary - get words by prefix
- /statistics - get statistics on handling the dictionary endpoint
- /update_dictionary - updates the dictionary with a new list of words
- /get_action_status - **extra endpoint - gives status on an action in the service - for example: status on updating the
  dictionary

#### Technical note - the service was developed in Python using the Fastapi framework

#### Assumptions

- Uploading a words file will be in text format
- The list of words in the dictionary will not exceed 204,833 and will be as a line-separated string
- The file given in the exercise can be loaded when the service is startup - just com

## Getting started

1. Installation
   1. python (3.7 or higher) on your machine
   2. pip
   3. conda or virtualenv - to create a virtual environment to work with
      1. pip install virtualenv
2. Clone the repo
   1. git clone <repo_url>
3. Create virtual environment (using virtualenv)
   1. cd <repo>
   2. virtualenv venv_name
   3. activate the env 
      1. mac - source venv_name/bin/activate
      2. win - venv_name/Scripts/activate.bat
4. install packages 
   1. pip install -r requirements.txt

##Run the service

Two options:
1. Run main.py from any IDE (make sure you have connected the IDE with the created virtual environment)
2. Run from terminal (env is activated) - uvicorn main:app --reload   

** The initial dictionary can be loaded when starting the service - just uncomment the function call
in orm_handler.words -  init_dictionary()

##Interaction with the service

Two options:
1. open the Swagger - http://localhost:8000/docs#
2. install Postman and run specific requests
