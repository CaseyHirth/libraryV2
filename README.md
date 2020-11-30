# Bridges library System 
A simple library manangement flask web app

# Requirements
* Python 3.8
* [Flask](http://flask.pocoo.org/docs/0.11/)  - Python Based Web Framework Used
* MySQL database
* WSGI or similar web service (production only)

## Installation
```
$ pip install flask
$ pip install mysql
```

## Setting up the virtual environment and installing other dependencies
```
$ source setup.sh
```

## Setup the Database
```
$ python3
>>>import models
>>> from app import db
>>> db.create_all()
>>> quit() to exit 
```


## Starting the Server/Running the app
```
$ python3 app.py
```

Or  
```
$ python3 flask run
```
## License 

This project is licensed under the MIT License - see the [MIT License](https://opensource.org/licenses/MIT) for details.
