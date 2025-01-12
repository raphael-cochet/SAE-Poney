from flask import render_template, session, url_for, request, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import Client, Moniteur, Poney, Cours, Reserver, CoursRegulier, CoursParticulier, Cotisation
from .app import app, db
from sqlalchemy import or_
from datetime import datetime, timedelta
from flask import jsonify

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

@app.route('/poneys', methods=['GET'])
def les_poneys():
    poneys = Poney.query.all()
    return render_template(
        "les_poneys.html",
        title="Les Poneys",
        search_route=url_for('les_poneys'),
        poneys=poneys
    )

# Dans views.py
from datetime import datetime, timedelta
from flask_login import current_user, login_required

@app.route('/creer_cours', methods=['GET', 'POST'])
@login_required
def creer_cours():
    if current_user.type != 'moniteur':
        flash('Accès réservé aux moniteurs', 'danger')
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        try:
            duree = int(request.form.get('duree'))
            nb_max = int(request.form.get('nb_max'))
            prix = float(request.form.get('prix'))
            heure = datetime.strptime(request.form.get('heure'), '%H:%M').time()
            type_cours = request.form.get('type_cours')
            
            cours_data = {
                'dureeCours': duree,
                'heureCours': heure,
                'prixCours': prix,
                'id_moniteur': current_user.id
            }
            
            if type_cours == 'regulier':
                cours_data['nbPersMax'] = nb_max
                jour = request.form.get('jour')
                nouveau_cours = CoursRegulier(
                    **cours_data,
                    jourCours=jour
                )
                
            elif type_cours == 'particulier':
                cours_data['nbPersMax'] = 1
                date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
                date_complete = datetime.combine(date, heure)
                id_client = int(request.form.get('client'))
                id_poney = int(request.form.get('poney'))
                
                nouveau_cours = CoursParticulier(
                    **cours_data,
                    dateCours=date_complete,
                    id_client=id_client,
                    id_poney=id_poney
                )
            
            db.session.add(nouveau_cours)
            db.session.commit()
            flash('Cours créé avec succès!', 'success')
            return redirect(url_for('planning'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la création du cours: {str(e)}', 'danger')
            
    clients = Client.query.all()
    poneys = Poney.query.all()
    return render_template('creer_cours.html', clients=clients, poneys=poneys)


@app.route('/inscription_cours/<int:cours_id>', methods=['POST'])
@login_required
def inscription_cours(cours_id):
    if current_user.type != 'client':
        flash('Accès réservé aux clients', 'danger')
        return redirect(url_for('planning'))
        
    cours = CoursRegulier.query.get_or_404(cours_id)
    
    # Vérifier si le cours n'est pas complet pour la prochaine séance
    today = datetime.today()
    prochaine_date = calculer_prochaine_date(cours.jourCours, cours.heureCours)
    
    nb_inscrits = Reserver.query.filter_by(
        id_cours=cours_id,
        dateCours=prochaine_date
    ).count()
    
    if nb_inscrits >= cours.nbPersMax:
        flash('Ce cours est complet pour la prochaine séance', 'danger')
        return redirect(url_for('planning'))
    
    # Vérifier si le client n'est pas déjà inscrit à ce cours
    deja_inscrit = Reserver.query.filter_by(
        id_cours=cours_id,
        id_client=current_user.id,
        dateCours=prochaine_date
    ).first()
    
    if deja_inscrit:
        flash('Vous êtes déjà inscrit à ce cours', 'danger')
        return redirect(url_for('planning'))
    
    # TODO: Ajouter la sélection du poney lors de l'inscription
    reservation = Reserver(
        id_cours=cours_id,
        id_client=current_user.id,
        dateCours=prochaine_date
    )
    
    try:
        db.session.add(reservation)
        db.session.commit()
        flash('Inscription réussie!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de l\'inscription: {str(e)}', 'danger')
        
    return redirect(url_for('planning'))


@app.route('/planning')
@login_required
def planning():
    # Récupérer tous les cours réguliers
    cours_reguliers = CoursRegulier.query\
        .order_by(CoursRegulier.jourCours, CoursRegulier.heureCours)\
        .all()
    
    # Récupérer les cours particuliers pour la semaine à venir
    today = datetime.today()
    une_semaine = today + timedelta(days=7)
    
    cours_particuliers = CoursParticulier.query\
        .filter(CoursParticulier.dateCours.between(today, une_semaine))\
        .order_by(CoursParticulier.dateCours)\
        .all()
    
    # Formatage pour le template
    cours_reguliers_formated = []
    for c in cours_reguliers:
        cours_reguliers_formated.append({
            'idCours': c.idCours,
            'jourCours': c.jourCours,
            'heureCours': c.heureCours.strftime('%H:%M'),
            'dureeCours': c.dureeCours,
            'prixCours': c.prixCours,
            'nbPersMax': c.nbPersMax,
            'moniteur': {
                'prenom': c.moniteur.prenom,
                'nom': c.moniteur.nom
            }
        })
    
    cours_particuliers_formated = []
    for c in cours_particuliers:
        cours_particuliers_formated.append({
            'idCours': c.idCours,
            'dateCours': c.dateCours.strftime('%Y-%m-%d'),
            'heureCours': c.heureCours.strftime('%H:%M'),
            'dureeCours': c.dureeCours,
            'prixCours': c.prixCours,
            'moniteur': {
                'prenom': c.moniteur.prenom,
                'nom': c.moniteur.nom
            },
            'client': {
                'prenom': c.client.prenom,
                'nom': c.client.nom
            } if c.client else None
        })
    
    return render_template(
        'planning.html',
        cours_reguliers=cours_reguliers_formated,
        cours_particuliers=cours_particuliers_formated
    )

def calculer_prochaine_date(jour_cours, heure_cours):
    """Calcule la prochaine date pour un cours régulier"""
    today = datetime.today()
    jours = {
        'Lundi': 0, 'Mardi': 1, 'Mercredi': 2,
        'Jeudi': 3, 'Vendredi': 4, 'Samedi': 5, 'Dimanche': 6
    }
    jour_cours_num = jours[jour_cours]
    jours_a_ajouter = (jour_cours_num - today.weekday() + 7) % 7
    if jours_a_ajouter == 0 and today.time() > heure_cours:
        jours_a_ajouter = 7
    prochaine_date = today + timedelta(days=jours_a_ajouter)
    return datetime.combine(prochaine_date.date(), heure_cours)



@app.route('/reservations', methods=['GET'])
def get_reservations():
    reservations = Reserver.query.all()
    return jsonify([r.to_dict() for r in reservations])
