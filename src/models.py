from .app import db
from datetime import datetime

class Personne(db.Model):
    __tablename__ = 'personne'
    idP = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomP = db.Column(db.String(100), nullable=False)
    prenomP = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'personne',
        'polymorphic_on': type
    }

class Moniteur(Personne):
    __tablename__ = 'moniteur'
    idP = db.Column(db.Integer, db.ForeignKey('personne.idP'), primary_key=True)
    idMoniteur = db.Column(db.Integer, unique=True)
    cours = db.relationship('Cours', backref='moniteur')
    __mapper_args__ = {
        'polymorphic_identity': 'moniteur',
    }

class Client(Personne):
    __tablename__ = 'client'
    idP = db.Column(db.Integer, db.ForeignKey('personne.idP'), primary_key=True)
    idC = db.Column(db.Integer, unique=True)
    poidsC = db.Column(db.Float)
    cotisations = db.relationship('Cotisation', backref='client')
    reservations = db.relationship('Reserver', backref='client')
    __mapper_args__ = {
        'polymorphic_identity': 'client',
    }

class Cours(db.Model):
    __tablename__ = 'cours'
    idCours = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nbPersMax = db.Column(db.Integer, nullable=False)
    dureeCours = db.Column(db.Integer, nullable=False)
    jourCours = db.Column(db.Date, nullable=False)
    heureCours = db.Column(db.Time, nullable=False)
    prixCours = db.Column(db.Float, nullable=False)
    idMoniteur = db.Column(db.Integer, db.ForeignKey('moniteur.idP'))
    cours_realises = db.relationship('CoursRealise', backref='cours')

class CoursRealise(db.Model):
    __tablename__ = 'cours_realise'
    idCours = db.Column(db.Integer, db.ForeignKey('cours.idCours'), primary_key=True)
    dateCours = db.Column(db.Date, primary_key=True)

class Poney(db.Model):
    __tablename__ = 'poney'
    idPoney = db.Column(db.Integer, primary_key=True, autoincrement=True)
    poidMaxPoney = db.Column(db.Float, nullable=False)
    nomPoney = db.Column(db.String(100), nullable=False)
    reservations = db.relationship('Reserver', backref='poney')

class Cotisation(db.Model):
    __tablename__ = 'cotisation'
    idCotisation = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateRegCoti = db.Column(db.Date)
    prixCoti = db.Column(db.Float, nullable=False)
    idC = db.Column(db.Integer, db.ForeignKey('client.idP'))

class Reserver(db.Model):
    __tablename__ = 'reserver'
    idCours = db.Column(db.Integer, primary_key=True)
    dateCours = db.Column(db.Date, primary_key=True)
    idPoney = db.Column(db.Integer, db.ForeignKey('poney.idPoney'), primary_key=True)
    idC = db.Column(db.Integer, db.ForeignKey('client.idP'), primary_key=True)