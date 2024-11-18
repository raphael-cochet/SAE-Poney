from flask import Flask
from .app import app, db
from .views import *
from .commands import *
import src.views
import src.commands
import src.models