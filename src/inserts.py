from datetime import datetime
from app import db
from models import Personne, Client, Cotisation, Moniteur, Cours, CoursRealise, Poney, Reserver

# Création des personnes
personnes = [
 Personne(idP=1, nomP='Dupont', prenomP='Jean'),
 Personne(idP=2, nomP='Martin', prenomP='Sophie'),
 Personne(idP=3, nomP='Durand', prenomP='Paul'),
 Personne(idP=4, nomP='Leroy', prenomP='Emma')
]

# Création des clients
clients = [
 Client(idP=1, poidCl=75.0),
 Client(idP=2, poidCl=62.0)
]

# Création des cotisations
cotisations = [
 Cotisation(idCotisation=1, dateRegCoti=datetime.strptime('2024-01-11', '%Y-%m-%d').date(), prixCoti=11.5),
 Cotisation(idCotisation=2, dateRegCoti=datetime.strptime('2023-10-11', '%Y-%m-%d').date(), prixCoti=15.5)
]

# Création des moniteurs
moniteurs = [
 Moniteur(idP=3),
 Moniteur(idP=4)
]

# Création des cours
cours = [
 Cours(idCours=101, nbPersMax=10, dureeCours=60, jourCours=datetime.strptime('2023-10-01', '%Y-%m-%d').date(),
 heureCours=datetime.strptime('10:00:00', '%H:%M:%S').time(), idMoniteur=3),
 Cours(idCours=102, nbPersMax=8, dureeCours=45, jourCours=datetime.strptime('2023-10-02', '%Y-%m-%d').date(),
 heureCours=datetime.strptime('14:00:00', '%H:%M:%S').time(), idMoniteur=4)
]

# Création des cours réalisés
cours_realises = [
 CoursRealise(idCours=101, dateCours=datetime.strptime('2023-10-01', '%Y-%m-%d').date()),
 CoursRealise(idCours=102, dateCours=datetime.strptime('2023-10-02', '%Y-%m-%d').date())
]

# Création des poneys
poneys = [
 Poney(idPoney=201, poidMaxPoney=200.0, nomPoney='Flash'),
 Poney(idPoney=202, poidMaxPoney=180.0, nomPoney='Spirit')
]

# Création des réservations
reservations = [
 Reserver(idCours=101, dateCours=datetime.strptime('2023-10-01', '%Y-%m-%d').date(), idPoney=201, idCl=1),
 Reserver(idCours=102, dateCours=datetime.strptime('2023-10-02', '%Y-%m-%d').date(), idPoney=202, idCl=2)
]

try:
 db.session.add_all(personnes)
 db.session.add_all(clients)
 db.session.add_all(cotisations)
 db.session.add_all(moniteurs)
 db.session.add_all(cours)
 db.session.add_all(cours_realises)
 db.session.add_all(poneys)
 db.session.add_all(reservations)

 db.session.commit()
 print("Les données ont été insérées avec succès.")

except Exception as e:
 db.session.rollback()
 print(f"Une erreur est survenue lors de l'insertion des données : {e}")

finally:
 db.session.close()