import imp
from flask import Flask
from os import path
from flask_login import LoginManager
from .views import views
from .auth import auth
from .models import User, Note
from .db import db

DB_NAME = "database.db"

#Creates an instance of flask
app = Flask(__name__)

def create_app():
    
    app.config['SECRET_KEY'] = 'dorl'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #Initalize Db
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

@app.before_first_request
def create_database():
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created Database!')

