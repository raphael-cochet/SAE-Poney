from app import db
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for
from datetime import date, time
from validators import (
 check_nb_pers_max,
 check_poney_pause,
 check_poney_poids,
 check_moniteur_cours_particulier,
 check_cotisation_paye
)

class Personne(db.Model):
 __tablename__ = 'personne'
 
 idP = db.Column(db.Integer, primary_key=True)
 nomP = db.Column(db.String(42), nullable=False)
 prenomP = db.Column(db.String(42), nullable=False)
 
 # Relations
 client = relationship('Client', back_populates='personne', uselist=False)
 moniteur = relationship('Moniteur', back_populates='personne', uselist=False)


class Client(db.Model):
 __tablename__ = 'client'
 
 idP = db.Column(db.Integer, db.ForeignKey('personne.idP'), primary_key=True)
 poidCl = db.Column(db.Float, nullable=False)
 
 # Relation avec Personne
 personne = relationship('Personne', back_populates='client')


class Cotisation(db.Model):
 __tablename__ = 'cotisation'
 
 idCotisation = db.Column(db.Integer, primary_key=True)
 dateRegCoti = db.Column(db.Date, nullable=False)
 prixCoti = db.Column(db.Float, nullable=False)


class Moniteur(db.Model):
 __tablename__ = 'moniteur'
 
 idP = db.Column(db.Integer, db.ForeignKey('personne.idP'), primary_key=True)
 
 # Relation avec Personne
 personne = relationship('Personne', back_populates='moniteur')
 cours = relationship('Cours', back_populates='moniteur')


class Cours(db.Model):
 __tablename__ = 'cours'
 
 idCours = db.Column(db.Integer, primary_key=True)
 nbPersMax = db.Column(db.Integer, nullable=False)
 dureeCours = db.Column(db.Integer, nullable=False)
 jourCours = db.Column(db.Date, nullable=False)
 heureCours = db.Column(db.Time, nullable=False)
 idMoniteur = db.Column(db.Integer, db.ForeignKey('moniteur.idP'), nullable=False)
 
 # Contraintes
 __table_args__ = (CheckConstraint("dureeCours IN (1, 2)", name="check_duree_cours"),)
 
 # Relations
 moniteur = relationship('Moniteur', back_populates='cours')
 cours_realises = relationship('CoursRealise', back_populates='cours')


class CoursRealise(db.Model):
 __tablename__ = 'cours_realise'
 
 idCours = db.Column(db.Integer, db.ForeignKey('cours.idCours'), primary_key=True)
 dateCours = db.Column(db.Date, primary_key=True)
 
 # Relations
 cours = relationship('Cours', back_populates='cours_realises')
 reservations = relationship('Reserver', back_populates='cours_realise')


class Poney(db.Model):
 __tablename__ = 'poney'
 
 idPoney = db.Column(db.Integer, primary_key=True)
 poidMaxPoney = db.Column(db.Float, nullable=False)
 nomPoney = db.Column(db.String(42), nullable=False)
 
 # Relation avec Reserver
 reservations = relationship('Reserver', back_populates='poney')


class Reserver(db.Model):
 __tablename__ = 'reserver'
 
 idCours = db.Column(db.Integer, primary_key=True)
 dateCours = db.Column(db.Date, primary_key=True)
 idPoney = db.Column(db.Integer, db.ForeignKey('poney.idPoney'), primary_key=True)
 idCl = db.Column(db.Integer, db.ForeignKey('client.idP'), primary_key=True)
 
 # Relations
 cours_realise = relationship('CoursRealise', back_populates='reservations')
 client = relationship('Client')
 poney = relationship('Poney', back_populates='reservations')


# Ajouter les événements pour les validations
@listens_for(Reserver, 'before_insert')
def before_insert_reservation(mapper, connect, target):
 session = db.Session(bind=connect)

 # Contrainte 1: Limite de 10 personnes par cours
 check_nb_pers_max(session, target.idCours, target.dateCours)

 # Contrainte 2: Pause d'une heure pour les poneys
 check_poney_pause(session, target.idPoney, target.idCours, target.dateCours)

 # Contrainte 3: Poids du cavalier
 check_poney_poids(session, target.idPoney, target.idCl)

 # Contrainte 4: Cours particulier pour un moniteur
 cours = session.query(Cours).filter_by(idCours=target.idCours).first()
 check_moniteur_cours_particulier(session, cours.idMoniteur, target.dateCours, cours.heureCours)

 # Contrainte 5: Cotisation payée
 check_cotisation_paye(session, target.idCl)


@listens_for(Reserver, 'before_update')
def before_update_reservation(mapper, connect, target):
 session = db.Session(bind=connect)

 # Appliquer les mêmes validations que pour l'insertion
 check_nb_pers_max(session, target.idCours, target.dateCours)
 check_poney_pause(session, target.idPoney, target.idCours, target.dateCours)
 check_poney_poids(session, target.idPoney, target.idCl)
 cours = session.query(Cours).filter_by(idCours=target.idCours).first()
 check_moniteur_cours_particulier(session, cours.idMoniteur, target.dateCours, cours.heureCours)
 check_cotisation_paye(session, target.idCl)