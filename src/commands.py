import click
from .app import app, db
import yaml
from datetime import datetime, time

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    """Creates the tables and populates them with data, avoiding duplicates."""
    db.create_all()
    
    with open(filename, 'r') as f:
        data = yaml.safe_load(f)

    from .models import Personne, Client, Moniteur, Poney, CoursRegulier, CoursParticulier, Reserver, Cotisation

    # Création des clients
    for cl in data.get("clients", []):
        client = Client.query.filter_by(mail=cl["mail"]).first()
        if client is None:
            client_data = {
                'id': cl['id'],
                'nom': cl['nomP'],
                'prenom': cl['prenomP'],
                'mail': cl['mail'],
                'type': 'client',
                'poids': cl['poidsC']
            }
            client = Client(**client_data)
            db.session.add(client)
        else:
            print(f"Client {cl['nomP']} {cl['prenomP']} déjà existant.")

    # Création des moniteurs
    for mo in data.get("moniteurs", []):
        moniteur = Moniteur.query.filter_by(mail=mo["mail"]).first()
        if moniteur is None:
            moniteur_data = {
                'id': mo['id'],
                'nom': mo['nomP'],
                'prenom': mo['prenomP'],
                'mail': mo['mail'],
                'type': 'moniteur'
            }
            moniteur = Moniteur(**moniteur_data)
            db.session.add(moniteur)
        else:
            print(f"Moniteur {mo['nomP']} {mo['prenomP']} déjà existant.")

    # Création des poneys
    for po in data.get("poneys", []):
        poney = Poney.query.filter_by(idPoney=po["idPoney"]).first()
        if poney is None:
            poney = Poney(**po)
            db.session.add(poney)
        else:
            print(f"Poney {po['nomPoney']} déjà existant.")

    # On fait un premier commit pour avoir les IDs des entités créées
    db.session.commit()

    # Création des cours réguliers
    for co in data.get("cours_reguliers", []):
        cours = CoursRegulier.query.filter_by(idCours=co["idCours"]).first()
        if cours is None:
            heure = datetime.strptime(co['heureCours'], '%H:%M').time()
            cours_data = {
                'idCours': co['idCours'],
                'nbPersMax': co['nbPersMax'],
                'dureeCours': co['dureeCours'],
                'jourCours': co['jourCours'],
                'heureCours': heure,
                'prixCours': co['prixCours'],
                'id_moniteur': co['id_moniteur']
            }
            cours = CoursRegulier(**cours_data)
            db.session.add(cours)
        else:
            print(f"Cours régulier {co['idCours']} déjà existant.")

    # Création des cours particuliers
    for cp in data.get("cours_particuliers", []):
        cours = CoursParticulier.query.filter_by(idCours=cp["idCours"]).first()
        if cours is None:
            date_cours = datetime.strptime(cp['dateCours'], '%Y-%m-%d %H:%M:%S')
            cours_data = {
                'idCours': cp['idCours'],
                'nbPersMax': 1,
                'dureeCours': cp['dureeCours'],
                'heureCours': date_cours.time(),
                'prixCours': cp['prixCours'],
                'id_moniteur': cp['id_moniteur'],
                'dateCours': date_cours,
                'id_client': cp['id_client'],
                'id_poney': cp['id_poney']
            }
            cours = CoursParticulier(**cours_data)
            db.session.add(cours)
        else:
            print(f"Cours particulier {cp['idCours']} déjà existant.")

    # Création des réservations
    for re in data.get("reservations", []):
        reservation = Reserver.query.filter_by(id=re["id"]).first()
        if reservation is None:
            date_cours = datetime.strptime(re['dateCours'], '%Y-%m-%d %H:%M:%S')
            reservation_data = {
                'id': re['id'],
                'id_cours': re['id_cours'],
                'id_client': re['id_client'],
                'id_poney': re['id_poney'],
                'dateCours': date_cours
            }
            reservation = Reserver(**reservation_data)
            db.session.add(reservation)
        else:
            print(f"Réservation {re['id']} déjà existante.")

    # Création des cotisations
    for co in data.get("cotisations", []):
        cotisation = Cotisation.query.filter_by(idCotisation=co["idCotisation"]).first()
        if cotisation is None:
            date_cotisation = datetime.strptime(co['dateRecCoti'], '%Y-%m-%d').date()
            cotisation_data = {
                'idCotisation': co['idCotisation'],
                'dateRecCoti': date_cotisation,
                'prixCoti': co['prixCoti'],
                'id_client': co['id_client']
            }
            cotisation = Cotisation(**cotisation_data)
            db.session.add(cotisation)
        else:
            print(f"Cotisation {co['idCotisation']} déjà existante.")

    # Commit final
    db.session.commit()

@app.cli.command()
def syncdb():
    '''Creates all missing tables.'''
    db.create_all()

@app.cli.command()
@click.argument('username')
@click.argument('password')
def newuser(username, password):
    '''Adds a new user.'''
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    from .models import Client
    client = Client(
        nom=username,
        prenom="",
        mail=f"{username}@email.com",
        type="client",
        poids=0,
        mot_de_passe=m.hexdigest()
    )
    db.session.add(client)
    db.session.commit()