from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .api import api
from flasgger import Swagger

from .database import db

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    swagger = Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "WhoIntedMe API",
            "version": "1.0",
            "description": "API for the WhoIntedMe project"
        }
    })
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('front/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
