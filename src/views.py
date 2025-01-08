from flask import render_template, url_for
from .app import app, db


@app.route("/")
def home():
    return render_template(
        "accueil.html",
        title="Accueil",
        search_route=url_for('home')
    )



@app.route('/les-cours')
def les_cours():
    return render_template('les_cours.html')

@app.route('/planning')
def planning():
    return render_template('planning.html')

@app.route('/poneys')
def les_poneys():
    return render_template(
        "les_poneys.html",
        title="Les Poneys",
        search_route=url_for('les_poneys')
    )