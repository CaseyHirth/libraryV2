# Bridges Library System 
A simple library management flask web app

## Requirements
* Python 3.8
* [Flask](http://flask.pocoo.org/docs/0.11/)  - Python Based Web Framework Used
* MySQL database

## Installation
```
$ pip install flask
$ pip install mysql
```

## Setting up the virtual environment and installing other dependencies

In order to do this, type: ```source setup.sh``` into the Linux terminal. Make sure that you have [Bash shell](https://www.gnu.org/software/bash/manual/html_node/Basic-Installation.html) command configured on your system. 
```
$ source setup.sh
```

## Setting up the Database
To connect the app to your database using Mysql Workbench or the terminal, make sure you change the ```highlighted lines``` in the app.py file with your d database details:
```
app.config['SECRET_KEY'] = 'PUT YOUR SECRET CODE HERE'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password/database-name'
```
## Starting the Server/Running the app
```
$ python3 run.py
```

Or  
```
$ python3 flask run
```
If you are successful you will see something like:  
```
Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

and click the link in your terminal to check if it deployed correctly.
```
## License 

This project is licensed under the MIT License - see the [MIT License](https://opensource.org/licenses/MIT) for details.
