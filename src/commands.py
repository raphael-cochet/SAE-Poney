import click
import yaml
from .app import app, db
from datetime import datetime
from .models import Personne, Client, Cotisation, Moniteur, Cours, CoursRealise, Poney, Reserver


@app.cli.command()
@click.argument("filename")
def loaddb(filename):
    """Creates the tables and populates them with data from a YAML file, avoiding duplicates."""
    db.create_all()  # Crée les tables
    print("Les tables ont été créées avec succès.")

    # Charger les données à partir du fichier YAML
    with open(filename, "r") as file:
        data = yaml.safe_load(file)

    # Insérer les personnes
    for person in data.get("personnes", []):
        existing = Personne.query.filter_by(idP=person["idP"]).first()
        if not existing:
            db.session.add(Personne(**person))
        else:
            print(f"Personne {person['nomP']} {person['prenomP']} déjà existante.")

    # Insérer les clients
    for client in data.get("clients", []):
        existing = Client.query.filter_by(idP=client["idP"]).first()
        if not existing:
            db.session.add(Client(**client))
        else:
            print(f"Client {client['idP']} déjà existant.")

    # Insérer les cotisations
    for cotisation in data.get("cotisations", []):
        existing = Cotisation.query.filter_by(idCotisation=cotisation["idCotisation"]).first()
        if not existing:
            db.session.add(Cotisation(**cotisation))
        else:
            print(f"Cotisation {cotisation['idCotisation']} déjà existante.")

    # Insérer les moniteurs
    for moniteur in data.get("moniteurs", []):
        existing = Moniteur.query.filter_by(idP=moniteur["idP"]).first()
        if not existing:
            db.session.add(Moniteur(**moniteur))
        else:
            print(f"Moniteur {moniteur['idP']} déjà existant.")

    # Insérer les cours
    for cour in data.get("cours", []):
        existing = Cours.query.filter_by(idCours=cour["idCours"]).first()
        if not existing:
            # Convertir les dates et heures
            cour["jourCours"] = datetime.strptime(cour["jourCours"], "%Y-%m-%d").date()
            cour["heureCours"] = datetime.strptime(cour["heureCours"], "%H:%M:%S").time()
            db.session.add(Cours(**cour))
        else:
            print(f"Cours {cour['idCours']} déjà existant.")

    # Insérer les cours réalisés
    for cr in data.get("cours_realises", []):
        existing = CoursRealise.query.filter_by(idCours=cr["idCours"], dateCours=cr["dateCours"]).first()
        if not existing:
            cr["dateCours"] = datetime.strptime(cr["dateCours"], "%Y-%m-%d").date()
            db.session.add(CoursRealise(**cr))
        else:
            print(f"Cours réalisé {cr['idCours']} à la date {cr['dateCours']} déjà existant.")

    # Insérer les poneys
    for poney in data.get("poneys", []):
        existing = Poney.query.filter_by(idPoney=poney["idPoney"]).first()
        if not existing:
            db.session.add(Poney(**poney))
        else:
            print(f"Poney {poney['nomPoney']} déjà existant.")

    # Insérer les réservations
    for reservation in data.get("reservations", []):
        existing = Reserver.query.filter_by(
            idCours=reservation["idCours"],
            dateCours=reservation["dateCours"],
            idPoney=reservation["idPoney"],
            idCl=reservation["idCl"],
        ).first()
        if not existing:
            reservation["dateCours"] = datetime.strptime(reservation["dateCours"], "%Y-%m-%d").date()
            db.session.add(Reserver(**reservation))
        else:
            print(f"Réservation {reservation} déjà existante.")

    db.session.commit()
    print("Les données ont été insérées avec succès.")


@app.cli.command()
def syncdb():
    """Creates all missing tables."""
    db.create_all()
    print("Les tables ont été créées avec succès.")

@app.cli.command()
def dropdb():
    """Creates all missing tables."""
    db.drop_all()
    print("Les tables ont été détruites avec succès.")