from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta

def check_nb_pers_max(session: Session, id_cours, date_cours):
    from .models import Reserver, Cours
    cours = session.query(Cours).filter_by(idCours=id_cours).first()
    if not cours:
        raise ValueError("Le cours spécifié n'existe pas")
    
    count = session.query(Reserver).filter_by(idCours=id_cours, dateCours=date_cours).count()
    if count >= cours.nbPersMax:
        raise ValueError(f"Le cours ne peut pas dépasser {cours.nbPersMax} personnes")

def check_poney_pause(session: Session, id_poney, id_cours, date_cours):
    from .models import Reserver, Cours
    cours = session.query(Cours).filter_by(idCours=id_cours).first()
    if not cours:
        raise ValueError("Le cours spécifié n'existe pas")
    
    heure_cours = cours.heureCours
    heure_fin = (datetime.combine(date.today(), heure_cours) + timedelta(hours=cours.dureeCours)).time()

    dernier_cours = (session.query(Cours)
                    .join(Reserver)
                    .filter(Reserver.idPoney == id_poney, 
                           Reserver.dateCours == date_cours)
                    .order_by(Cours.heureCours.desc())
                    .first())
    
    if dernier_cours:
        derniere_fin = (datetime.combine(date.today(), dernier_cours.heureCours) 
                       + timedelta(hours=dernier_cours.dureeCours)).time()
        if derniere_fin > (datetime.combine(date.today(), heure_cours) 
                          - timedelta(hours=1)).time():
            raise ValueError("Le poney doit avoir 1h de pause entre les cours")

def check_poney_poids(session: Session, id_poney, id_client):
    from .models import Client, Poney
    client = session.query(Client).filter_by(idP=id_client).first()
    poney = session.query(Poney).filter_by(idPoney=id_poney).first()
    
    if not client or not poney:
        raise ValueError("Le client ou le poney spécifié n'existe pas")
    
    if client.poidsC > poney.poidMaxPoney:
        raise ValueError("Le cavalier dépasse le poids limite du poney")

def check_cotisation_valide(session: Session, id_client):
    from .models import Cotisation
    cotisation = (session.query(Cotisation)
                 .filter_by(idC=id_client)
                 .order_by(Cotisation.dateRegCoti.desc())
                 .first())
    
    if not cotisation or not cotisation.dateRegCoti:
        raise ValueError("L'adhérent doit avoir une cotisation valide")
    
    date_expiration = cotisation.dateRegCoti.replace(year=cotisation.dateRegCoti.year + 1)
    if date.today() > date_expiration:
        raise ValueError("La cotisation n'est plus valide")