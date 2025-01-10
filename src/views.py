from flask import render_template, session, url_for, request, redirect, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from .models import Client, Moniteur
from .app import app, db

@app.route("/")
def home():
    return render_template(
        "accueil.html",
        title="Accueil",
        search_route=url_for('home')
    )

@app.route('/creer_compte', methods=['GET', 'POST'])
def creer_compte():
    session.pop('_flashes', None)
    if request.method == 'POST':
        print("Données du formulaire reçues")
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        type_compte = request.form.get('type')
        email = request.form.get('identifiant')
        password = request.form.get('password')

        print(f"Données reçues : {nom}, {prenom}, {type_compte}, {email}")

        if not all([nom, prenom, type_compte, email, password]):
            flash('Tous les champs sont obligatoires.', 'danger')
            return redirect(url_for('creer_compte'))

        try:
            hashed_password = generate_password_hash(password)

            if type_compte == 'client':
                new_user = Client(
                    nom=nom,
                    prenom=prenom,
                    mail=email,
                    mot_de_passe=hashed_password,
                    type='client',
                    poids=0.0
                )
            elif type_compte == 'moniteur':
                new_user = Moniteur(
                    nom=nom,
                    prenom=prenom,
                    mail=email,
                    mot_de_passe=hashed_password,
                    type='moniteur'
                )
            else:
                flash('Type de compte invalide.', 'danger')
                return redirect(url_for('creer_compte'))

            print("Tentative d'ajout à la base de données")
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user)
            
            flash('Compte créé avec succès !', 'success')
            return redirect(url_for('home'))

        except Exception as e:
            print(f"Erreur lors de la création : {str(e)}")
            db.session.rollback()
            flash(f'Une erreur est survenue lors de la création du compte: {str(e)}', 'danger')
            return redirect(url_for('creer_compte'))

    return render_template('page_creer_compte.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifiant = request.form.get('identifiant')
        password = request.form.get('password')

        if not identifiant or not password:
            flash('Veuillez remplir tous les champs.', 'danger')
            print("Flash : Veuillez remplir tous les champs.")
            return redirect(url_for('login'))

        user = Client.query.filter_by(mail=identifiant).first()

        if user is None:
            user = Moniteur.query.filter_by(mail=identifiant).first()

        if user and check_password_hash(user.mot_de_passe, password):
            login_user(user)
            flash('Connexion réussie !', 'success')
            print("Flash : Connexion réussie !")
            return redirect(url_for('home'))
        else:
            flash('Identifiant ou mot de passe incorrect.', 'danger')
            print("Flash : Identifiant ou mot de passe incorrect.")
            return redirect(url_for('login'))

    return render_template("login.html", title="Login")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    return redirect(url_for('home'))

@app.route('/les-cours')
def les_cours():
    return render_template('page_cours.html')

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
