from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from models import Reserver, Cours, Client, Poney, Cotisation

# Contrainte 1: Un cours ne peut pas dépasser 10 personnes
def check_nb_pers_max(session: Session, id_cours, date_cours):
    count = session.query(Reserver).filter_by(idCours=id_cours, dateCours=date_cours).count()
    if count >= 10:
        raise ValueError("Le cours ne peut pas dépasser 10 personnes")

# Contrainte 2: Un poney ne peut pas être utilisé après un cours sans 1h de pause
def check_poney_pause(session: Session, id_poney, id_cours, date_cours):
    cours = session.query(Cours).filter_by(idCours=id_cours).first()
    if not cours:
        raise ValueError("Le cours spécifié n'existe pas.")
    
    heure_cours = cours.heureCours
    duree_cours = cours.dureeCours
    heure_fin = (datetime.combine(date.today(), heure_cours) + timedelta(hours=duree_cours)).time()

    dernier_cours = (session.query(Cours.heureCours)
                     .join(Reserver)
                     .filter(Reserver.idPoney == id_poney, Reserver.dateCours == date_cours)
                     .order_by(Cours.heureCours.desc())
                     .first())
    
    if dernier_cours and (datetime.combine(date.today(), dernier_cours[0]) + timedelta(hours=duree_cours)).time() > (heure_cours - timedelta(hours=1)):
        raise ValueError("Le poney ne peut pas être utilisé après un cours sans 1h de pause.")

# Contrainte 3: Un poney ne peut pas porter un cavalier supérieur à sa limite de poids
def check_poney_poids(session: Session, id_poney, id_client):
    client = session.query(Client).filter_by(idP=id_client).first()
    poney = session.query(Poney).filter_by(idPoney=id_poney).first()
    if not client or not poney:
        raise ValueError("Le client ou le poney spécifié n'existe pas.")
    if client.poidCl > poney.poidMaxPoney:
        raise ValueError("Le cavalier dépasse le poids limite du poney.")

# Contrainte 4: Un moniteur peut donner un cours particulier à un seul cavalier
def check_moniteur_cours_particulier(session: Session, id_moniteur, date_cours, heure_cours):
    nb_cours = (session.query(Reserver)
                .join(Cours)
                .filter(Cours.idMoniteur == id_moniteur, Reserver.dateCours == date_cours, Cours.heureCours == heure_cours)
                .count())
    if nb_cours > 0:
        raise ValueError("Le moniteur ne peut donner qu'un cours particulier à la fois à la même heure.")

# Contrainte 5: Les adhérents doivent régler une cotisation annuelle pour pouvoir réserver
def check_cotisation_paye(session: Session, id_client):
    cotisation = session.query(Cotisation).filter_by(idCotisation=id_client).first()
    if not cotisation or not cotisation.dateRegCoti:
        raise ValueError("L'adhérent doit régler sa cotisation annuelle pour pouvoir réserver.")
