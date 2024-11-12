from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
import os
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    app.config['SECRET_KEY'] = "3d02d25c-55ef-406a-b13d-666ef614b30c"
    
    def mkpath(p):
        return os.path.normpath(
            os.path.join(
                os.path.dirname(__file__),
                p))
    
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///" + mkpath("../myapp.db"))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bootstrap = Bootstrap5(app)

    with app.app_context():
        from .views import init_views
        init_views(app)

    return app
