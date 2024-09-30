INSERT INTO PERSONNE (idP, nomP, prenomP) VALUES
(1, 'Dupont', 'Jean'),
(2, 'Martin', 'Sophie'),
(3, 'Durand', 'Paul'),
(4, 'Leroy', 'Emma');

INSERT INTO CLIENT (idCl, poidCl, dateRegCoti) VALUES
(1, 75.0, '2023-01-15'),
(2, 62.0, '2023-02-20'); 

INSERT INTO MONITEUR (idMoniteur) VALUES
(3),
(4); 

INSERT INTO COURS (idCours, nbPersMax, dureeCours, jourCours, heureCours, idMoniteur) VALUES
(101, 10, 60, '2023-10-01', '10:00:00', 3), 
(102, 8, 45, '2023-10-02', '14:00:00', 4); 

INSERT INTO COURS_REALISE (idCours, dateCours) VALUES
(101, '2023-10-01'), 
(102, '2023-10-02');

INSERT INTO PONEY (idPoney, poidMaxPoney, nomPoney) VALUES
(201, 200.0, 'Flash'),
(202, 180.0, 'Spirit');

INSERT INTO RESERVER (idCours, dateCours, idPoney, idCl) VALUES
(101, '2023-10-01', 201, 1),
(102, '2023-10-02', 202, 2);
