from flask import render_template, url_for
from .app import db

def init_views(app):
    @app.route("/")
    def home():
        return render_template(
            "accueil.html",
            title="Accueil",
            search_route=url_for('home')
        )
