import os
from functools import wraps
from dotenv import load_dotenv
from www.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session, redirect, url_for
db = SQLAlchemy()

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if session:
            return view(*args, **kwargs)
        else:
            return redirect(url_for('auth_endpoints.login'))

    return wrapped_view

def create_app(config_class=Config):
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config[
        "SQLALCHEMY_DATABASE_URI"] = f"mysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWD']}@{os.environ['MYSQL_URL']}/{os.environ['MYSQL_DATABASE']}"
    db.init_app(app)

    from www.project.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from www.project.auth import auth_bp as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from www.project.query import query_bp as query_blueprint
    app.register_blueprint(query_blueprint)

    from www.project.livesearch import  livesearch_bp as livesearch_blueprint
    app.register_blueprint(livesearch_blueprint)

    from www.project.update import update_bp as update_blueprint
    app.register_blueprint(update_blueprint)

    return app

