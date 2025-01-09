from flask import render_template, url_for
from .app import app, db


@app.route("/")
def home():
    return render_template(
        "accueil.html",
        title="Accueil",
        search_route=url_for('home')
    )


@app.route("/login")
def login():
    return render_template(
        "login.html",
        title="login",
        search_route=url_for('login')
    )

@app.route('/creer_compte', methods=['GET', 'POST'])
def creer_compte():
    # if request.method == 'POST':
    #     nom = request.form['nom']
    #     prenom = request.form['prenom']
    #     identifiant = request.form['identifiant']
    #     mot_de_passe = request.form['password']

    #     if not nom or not prenom or not identifiant or not mot_de_passe:
    #         flash('Tous les champs sont obligatoires.', 'danger')
    #         return redirect(url_for('creer_compte'))

    #     if Personne.query.filter_by(mail=identifiant).first() is not None:
    #         flash("Cet identifiant est déjà  utilisé. Veuillez en choisir un autre.", "danger")
    #         return redirect(url_for('creer_compte'))

    #     mot_de_passe_hache = generate_password_hash(mot_de_passe)

    #     if fonction == 'Responsable':
    #         personne = ResponsableFormation(nom=nom, prenom=prenom, mail=identifiant, departement=departement, mot_de_passe=mot_de_passe_hache)
    #     elif fonction == 'Enseignant':
    #         personne = Enseignant(nom=nom, prenom=prenom, mail=identifiant, departement=departement, mot_de_passe=mot_de_passe_hache)
    #     elif fonction == 'Secretaire':
    #         personne = Secretaire(nom=nom, prenom=prenom, mail=identifiant, mot_de_passe=mot_de_passe_hache, departement=departement)
    #     else:
    #         flash("Fonction inconnue.", "danger")
    #         return redirect(url_for('creer_compte'))

    #     db.session.add(personne)
    #     db.session.commit()

    #     return redirect(url_for('connexion'))

    return render_template('page_creer_compte.html')



@app.route('/les-cours')
def les_cours():
    return render_template('les_cours.html')

@app.route('/planning')
def planning():
    return render_template('planning.html')

@app.route('/les-poneys')
def les_poneys():
    return render_template('les_poneys.html')

