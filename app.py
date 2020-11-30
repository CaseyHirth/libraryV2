from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
basePath = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(basePath, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret'

app.config['SQL_TRACK_MODIFICATION'] = False
app.config['SQL_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bf0cfce4e0806e:1d406a63@us-cdbr-east-02.cleardb.com/heroku_2da5a1a8a39f679'

db = SQLAlchemy(app)

Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#db = SQLAlchemy(app)
