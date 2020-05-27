# Warbler

Warbler is a Twitter clone that is built with Flask, JQuery, Bootstrap, Axios, and PostgreSQL

### Requirements

- PostgreSQL 12.2
- Python 3.8.2 or Later

### Installation

#### Setup

Create and activate a virtual environment.

```sh
python -m venv venv
```

```sh
source venv/Scripts/activate
```

##### Upgrade pip

```sh
(venv) $ pip install --upgrade pip
```

##### Installing dependencies

```sh
(venv) $ pip install -r requirements.txt
```

(optional) If the install fails you can manually install each dependency:

```sh
(venv) $ pip install flask
(venv) $ pip install flask-debugtoolbar
(venv) $ pip install psycopg2-binary
(venv) $ pip install flask-sqlalchemy
(venv) $ pip install flask-wtf
(venv) $ pip install bcrypt
```

#### Create the Databases

You will need to create two databases in PostgreSQL. One for the application and another for testing.

##### App Database

```sh
(venv) $ createdb warbler
(venv) $ python seed.py
```

##### Test Database

```sh
(venv) $ createdb warbler-test
```

#### Run Application

```sh
flask run
```

localhost:5000 or http://127.0.0.1:5000/ is the default location the application will run on.

#### Running Tests

```sh
FLASK_ENV=production python -m unittest <name-of-python-file>
```
