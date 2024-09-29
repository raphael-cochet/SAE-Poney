DROP TABLE IF EXISTS reserver;
DROP TABLE IF EXISTS poney;
DROP TABLE IF EXISTS cours;
DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS moniteur;
DROP TABLE IF EXISTS personne;

CREATE TABLE personne (
  idP INT PRIMARY KEY,
  nomP VARCHAR(42),
  prenomP VARCHAR(42)
);

CREATE TABLE client (
  idCl INT PRIMARY KEY,
  poidCl FLOAT, 
  dateRegCoti DATE,
  FOREIGN KEY (idCl) REFERENCES personne(idP)
);

CREATE TABLE moniteur (
  idMoniteur INT PRIMARY KEY,
  FOREIGN KEY (idMoniteur) REFERENCES personne(idP)
);

CREATE TABLE cours (
  idCours INT PRIMARY KEY,
  nbPersMax INT,
  dureeCours INT,
  jourCours DATE,
  heureCours TIME,
  idMoniteur INT NOT NULL,
  FOREIGN KEY (idMoniteur) REFERENCES moniteur(idMoniteur)
);

CREATE TABLE poney (
  idPoney INT PRIMARY KEY,
  poidMaxPoney FLOAT,
  nomPoney VARCHAR(42)
);

CREATE TABLE reserver (
  dateCours DATE,
  idPoney INT,
  idCl INT,
  PRIMARY KEY (dateCours, idPoney, idCl),
  FOREIGN KEY (idCl) REFERENCES client(idCl),
  FOREIGN KEY (idPoney) REFERENCES poney(idPoney)
);

