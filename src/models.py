from flask_login import UserMixin
from .app import db

class Personne(db.Model, UserMixin):
    __tablename__ = 'personne'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(100), unique=True, nullable=False)
    type = db.Column(db.String(50))
    
    __mapper_args__ = {
        'polymorphic_identity': 'personne',
        'polymorphic_on': type
    }

class Moniteur(Personne):
    __tablename__ = 'moniteur'
    id = db.Column(db.Integer, db.ForeignKey('personne.id'), primary_key=True)
    cours = db.relationship('Cours', backref='moniteur')
    
    __mapper_args__ = {
        'polymorphic_identity': 'moniteur',
    }

class Client(Personne):
    __tablename__ = 'client'
    id = db.Column(db.Integer, db.ForeignKey('personne.id'), primary_key=True)
    poids = db.Column(db.Float, nullable=False)
    cotisations = db.relationship('Cotisation', backref='client')
    reservations = db.relationship('Reserver', backref='client')
    
    __mapper_args__ = {
        'polymorphic_identity': 'client',
    }

class Cours(db.Model):
    __tablename__ = 'cours'
    idCours = db.Column(db.Integer, primary_key=True)
    nbPersMax = db.Column(db.Integer, nullable=False)
    dureeCours = db.Column(db.Integer, nullable=False)  # en heures
    jourCours = db.Column(db.String(20), nullable=False)
    heureCours = db.Column(db.Time, nullable=False)
    prixCours = db.Column(db.Float, nullable=False)
    id_moniteur = db.Column(db.Integer, db.ForeignKey('moniteur.id'))

class Reserver(db.Model):
    __tablename__ = 'reserver'
    id = db.Column(db.Integer, primary_key=True)
    id_cours = db.Column(db.Integer, db.ForeignKey('cours.idCours'))
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'))
    id_poney = db.Column(db.Integer, db.ForeignKey('poney.idPoney'))
    dateCours = db.Column(db.DateTime, nullable=False)

class Poney(db.Model):
    __tablename__ = 'poney'
    idPoney = db.Column(db.Integer, primary_key=True)
    nomPoney = db.Column(db.String(100), nullable=False)
    poidsMaxPoney = db.Column(db.Float, nullable=False)
    reservations = db.relationship('Reserver', backref='poney')

class Cotisation(db.Model):
    __tablename__ = 'cotisation'
    idCotisation = db.Column(db.Integer, primary_key=True)
    dateRecCoti = db.Column(db.Date, nullable=False)
    prixCoti = db.Column(db.Float, nullable=False)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'))