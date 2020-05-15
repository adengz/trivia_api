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

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
dropdb trivia
createdb trivia -O postgres
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Testing
To run the tests, run

```
dropdb trivia_test
createdb trivia_test
python test_flaskr.py
```


## API Documentation

### Endpoints
```
GET "/categories"
GET "/questions"
GET "/categories/<int:category>/questions"
POST "/questions"
POST "/questions/searches"
POST "/quizzes"
DELETE "/questions/<int:question_id>"
```

#### `GET "/categories"`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Request Arguments: None.
- Returns: An object with a single key, `"categories"`, that contains an object of id: category_string key:value pairs. 
- Response body:

```
"categories": {
	"1" : "NBA",
	...
}
```

#### `GET "/questions"`
- Fetches all questions, with pagination (10 per page by default).
- Request Arguments: int `page` page number, default to 1.
- Returns: An object with four keys, `"current_category"` (always to `null`), `"categories"` (same as `GET "/categories"`),  `"total_questions"`, to the total number of questions, `"questions"`, to the list of questions on the current page. 
- Response body:

```
"categories": {
	"1": "NBA",
	...
},
"current_category": null,
"questions": [
	{
		"answer": "Kobe 'Bean' Bryant#RIPMamba",
		"category": 1,
		"difficulty": 4,
		"id": 8,
		"question": "Which NBA legend has a middle name of 'Bean'?"
	},
	...
],
"total_questions": 24
```

#### `GET "/categories/<int:category>/questions"`
- Fetches all questions in a given category.
- Request Arguments: None.
- Returns: An object with three keys, `"current_category"` same as `category`, `"total_questions"`, to the total number of questions in this category, `"questions"`, to the list of questions in this category. 
- Response body:

```
"current_category": 1,
"questions": [
	{
		"answer": "Kobe 'Bean' Bryant#RIPMamba",
		"category": 1,
		"difficulty": 4,
		"id": 8,
		"question": "Which NBA legend has a middle name of 'Bean'?"
	},
	...
],
"total_questions": 5
```

#### `POST "/questions"`
- Adds a new question.
- Request Arguments (JSON): 
	- `"question"`: str of question
	- `"answer"`: str of answer
	- `"category"`: int of category id
	- `"difficulty"`: int of difficulty level from 1-5

```
"question": "Which NBA legend has a middle name of 'Bean'?",
"answer": "Kobe 'Bean' Bryant#RIPMamba",
"category": 1,
"difficulty": 4,
```
- Returns: None. 
- Response body: None.

#### `POST "/questions/searches"`
- Searches all questions in which the given search term is a substring.
- Request Arguments (JSON): str `"searchTerm"` pattern to search.

```
"searchTerm": "Bean"
```
- Returns: An object with three keys, `"current_category"` (always to `null`), `"total_questions"`, to the total number of questions in search result, `"questions"`, to the list of questions in search result. 
- Response body:

```
"current_category": null,
"questions": [
	{
		"answer": "Kobe 'Bean' Bryant#RIPMamba",
		"category": 1,
		"difficulty": 4,
		"id": 8,
		"question": "Which NBA legend has a middle name of 'Bean'?"
	},
	...
],
"total_questions": 1
```

#### `POST "/quizzes"`
- Fetches a new question in a selected category or all categories (`"id": 0`) not in previously asked questions.
- Request Arguments (JSON): 
	- `"previous_questions"`: list of ids of previously asked questions
	- `"quiz_category"`: dict containing the category id (0 for all categories) for current quiz

```
"previous_questions": [2, 5],
"quiz_category": {"id": 1}
```
- Returns: An object with a single key, `"question"`, mapping to a new question. 
- Response body:

```
"question": {
	"answer": "Kobe 'Bean' Bryant#RIPMamba",
	"category": 1,
	"difficulty": 4,
	"id": 8,
	"question": "Which NBA legend has a middle name of 'Bean'?"
}
```

#### `DELETE "/questions/<int:question_id>"`
- Deletes a question with given id.
- Request Arguments: None.
- Returns: None. 
- Response body: None.
