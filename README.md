# Full Stack Farm API for the capstone Project

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

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


## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py && export FLASK_ENV=development && flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py ` file to find the application. 

## REST API Documentation

This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/animals'
GET '/species'
POST '/animals'
PATCH '/animals'
DELETE '/animals'

GET '/animals'
- Fetches a dictionary of animals from the farm
- Request Arguments: None
- Returns: The dictionary of animals id and name. Also it returns the number of
animals and wether it was a success or not

```json
{
    "animals": {
        "1": "Freddy",
        "2": "Shao"
    },
    "number": 2,
    "success": true
}
```
GET '/species'
- Fetches a dictionary of species from the farm
- Request Arguments: None
- Returns: The number of the different species and a dictionary of species id and name
```json
{
    "number": 4,
    "species": {
        "1": "Dog",
        "2": "Cat",
        "3": "Panda",
        "4": "Guinea Pig"
    },
    "success": true
}
```
POST '/animals'
- Creates a new animal with the parameters name, age, comment and species id. Name and age are mandatory
- Request Arguments: None
- Request Headers:
---> insert (1. string - name; 2. integer - age; 3. string - comment; 4. integer - species_id)
- Example request JSON

```json
{
	"name": "Spikes",
	"species": "Guinea Pig",
    "age": 4,
    "comment": "Spike likes to run around.",
    "species_id": 4
}
```
-Returns: Example

```json
{
    "animal_created": "Spikes",
    "created": 3,
    "species": "Guinea Pig",
    "success": true,
    "total_animals": 3
}
```
DELETE '/animals/<int:animal_id>'
- Deletes the selected animal
- Request Arguments: animal id

-Returns: Example

```json
{
    "deleted": 3,
    "deleted name": "Spikes",
    "success": true,
    "total_animals": 2
}
```
## Authentification

Login: audience=https://capfarm.herokuapp.com&response_type=token
client_id=mKtioZo3JhgPPyeubzW4mm7qI7VdKAl1&redirect_uri=https://capfarm.herokuapp.com

## Testing
To run the tests, run
```
python test_app.py
```