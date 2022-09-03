from flask import Flask
import os
from dotenv import load_dotenv
from app.models import db, User, Task
from app.forms import LoginForm, RegisterForm


# create a flask app
my_app = Flask(__name__)

load_dotenv()
### important flask configuration for 'app'.
# Secret key is needed for cookies and session storage while the
# 'track_modifications = false' will silence the red warning thing.
my_app.secret_key = os.environ.get('APP_SECRET_KEY')
my_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('local_DATABASE_URL')
my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
my_app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ.get('RECAPTCHA_SITE_KEY')
my_app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get('RECAPTCHA_SECRET_KEY')
my_app.config['RECAPTCHA_OPTIONS'] = {'data-theme': 'dark'}

# this will link the flask app to the database.
db.init_app(my_app)


### from the python package named 'app', the 'views.py' model is being imported.
# this means you can access variables + functions from the module using dot notation.
# this import statement comes after app in intialised as the routes from views.py as that module will then call app
#   which has already been intialised in init.py
from app import views

views.login_manager.init_app(my_app)


with app.app_context():
    db.create_all()