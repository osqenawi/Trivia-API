# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.


### Setting environment variables

Before you run the server, you must create **.env** file
and include these environment variables in it:

**DEV_SQLALCHEMY_DATABASE_URI**: This variable should hava URI for Database that is used in development mode.

**TESTING_SQLALCHEMY_DATABASE_URI**: This variable should hava URI for Database that is used in testing mode.

From within the `backend` directory execute:

```bash
touch .env
open .env
```

Then include the environment variables in this file.

**For Example:**
* DEV_SQLALCHEMY_DATABASE_URI='postgres://osama@localhost:5432/trivia'

* TESTING_SQLALCHEMY_DATABASE_URI='postgres://osama@localhost:5432/trivia_test'

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### Database initialization

To load initial data into the database,
after running the server for the first time ever,
run this command once :

```bash
psql trivia < trivia.psql
```


### Testing

Tests run automatically every time the server run.


## API Reference

### Getting Started

* Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
* Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```bash
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:
* 400: Bad Request
* 404: Resource Not Found
* 405: Method Not Allowed
* 500: Internal Server Error

### Endpoint Library

**GET /categories**

* General:
    * Returns a dictionary that have id:type as a key:value pairs for each category.
    * Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

* Sample:  
  ```bash
  curl http://127.0.0.1:5000/categories
  ```
  ```json
  {
     "categories":{
        "1":"Science",
        "2":"Art",
        "3":"Geography",
        "4":"History",
        "5":"Entertainment",
        "6":"Sports"
     },
     "success":true
  }
  ```
  
**GET /questions**
* General:
    * Returns a categories, current_category, questions, success and total_questions.
    * Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
* Sample:  
  ```bash
  curl http://127.0.0.1:5000/questions?page=1
  ```
  ```json
  {
     "categories":{
        "1":"Science",
        "2":"Art",
        "3":"Geography",
        "4":"History",
        "5":"Entertainment",
        "6":"Sports"
     },
     "current_category":{
        "0":"click"
     },
     "questions":[
        {
           "answer":"Muhammad Ali",
           "category":"4",
           "difficulty":1,
           "id":2,
           "question":"What boxer's original name is Cassius Clay?"
        },
        {
           "answer":"Apollo 13",
           "category":"5",
           "difficulty":4,
           "id":3,
           "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
           "answer":"Tom Cruise",
           "category":"5",
           "difficulty":4,
           "id":4,
           "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
           "answer":"Edward Scissorhands",
           "category":"5",
           "difficulty":3,
           "id":5,
           "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
           "answer":"Brazil",
           "category":"6",
           "difficulty":3,
           "id":6,
           "question":"Which is the only team to play in every soccer World Cup tournament?"
        },
        {
           "answer":"Uruguay",
           "category":"6",
           "difficulty":4,
           "id":7,
           "question":"Which country won the first ever soccer World Cup in 1930?"
        },
        {
           "answer":"George Washington Carver",
           "category":"4",
           "difficulty":2,
           "id":8,
           "question":"Who invented Peanut Butter?"
        },
        {
           "answer":"Lake Victoria",
           "category":"3",
           "difficulty":2,
           "id":9,
           "question":"What is the largest lake in Africa?"
        },
        {
           "answer":"The Palace of Versailles",
           "category":"3",
           "difficulty":3,
           "id":10,
           "question":"In which royal palace would you find the Hall of Mirrors?"
        },
        {
           "answer":"Agra",
           "category":"3",
           "difficulty":2,
           "id":11,
           "question":"The Taj Mahal is located in which Indian city?"
        }
     ],
     "success":true,
     "total_questions":19
  }
  ```
  
**DELETE /questions/<id>**
* General:
    * Returns a deleted id and success value.
* Sample:  
  ```bash
  curl -X DELETE http://127.0.0.1:5000/questions/1
  ```
  ```json
  {
     "deleted":1,
     "success":true
  }
  ```
  
**POST /questions**
* General:
    * Returns a created id and success value.
    * Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

* Sample:  
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"question": "Ask?", "answer": "answered", "difficulty": 1, "category": "science"}' http://127.0.0.1:5000/questions
  ```
  ```json
  {
     "created":20,
     "success":true
  }
  ```
  
**POST /questionssearch**
* General:
    * Returns current_category, questions, success value and total_questions.
    * Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

* Sample:  
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}' http://127.0.0.1:5000/questionssearch
  ```
  ```json
  {
     "current_category":{
        "0":"click"
     },
     "questions":[
        {
           "answer":"Edward Scissorhands",
           "category":"5",
           "difficulty":3,
           "id":5,
           "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
     ],
     "success":true,
     "total_questions":1
  }
  ```
  
**GET /categories/<id>/questions**
* General:
    * Returns current_category, questions, success value and total_questions.
    * Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

* Sample:  
  ```bash
  curl  http://127.0.0.1:5000/categories/1/questions
  ```
  ```json
  {
     "current_category":{
        "1":"Science"
     },
     "questions":[
        {
           "answer":"The Liver",
           "category":"1",
           "difficulty":4,
           "id":16,
           "question":"What is the heaviest organ in the human body?"
        },
        {
           "answer":"Alexander Fleming",
           "category":"1",
           "difficulty":3,
           "id":17,
           "question":"Who discovered penicillin?"
        },
        {
           "answer":"Blood",
           "category":"1",
           "difficulty":4,
           "id":18,
           "question":"Hematology is a branch of medicine involving the study of what?"
        }
     ],
     "success":true,
     "total_questions":3
  }
  ```

**POST /quizzes**
* General:
    * Returns previous_questions, question and success value.

* Sample:  
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1, 9], "quiz_category": {"type": "Science", "id": "3"}}' http://127.0.0.1:5000/quizzes
  ```
  ```json
  {
     "previous_questions":[
        1,
        9,
        10
     ],
     "question":{
        "answer":"The Palace of Versailles",
        "category":"3",
        "difficulty":3,
        "id":10,
        "question":"In which royal palace would you find the Hall of Mirrors?"
     },
     "success":true
  }
  ```
  