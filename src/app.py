from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap5(app)

def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p))

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + mkpath("../myapp.db"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "21788944-5131-46d6-9b18-8eb01323b575"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from .models import Personne
    return Personne.query.get(int(user_id))

from .models import *

with app.app_context():
    db.create_all()

from .views import *
from .commands import *