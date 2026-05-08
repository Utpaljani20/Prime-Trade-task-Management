from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import os
db=SQLAlchemy()
jwt=JWTManager()
bcrypt=Bcrypt()

def create_app():
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../static/templates')

    # Configuration
    app.config['SECRET_KEY'] = 'woh-hai'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TaskManagement.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'Joh-hai' 

    # Plugins ko app ke saath connect karo
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    # Blueprints register karna (Auth aur CRUD routes ke liye)
    from .auth import auth_bp
    from .crud import crud_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(crud_bp, url_prefix='/api')

    with app.app_context():
        db.create_all() # Database automatically ban jayega

    return app

