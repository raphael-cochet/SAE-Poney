INSERT INTO personne (idP, nomP, prenomP) VALUES
(1, 'Dupont', 'Jean'),
(2, 'Martin', 'Sophie'),
(3, 'Durand', 'Paul'),
(4, 'Leroy', 'Emma');

INSERT INTO client (idCl, poidCl, dateRegCoti) VALUES
(1, 75.0, '2023-01-15'), -- Jean Dupont
(2, 62.0, '2023-02-20'); -- Sophie Martin

INSERT INTO moniteur (idMoniteur) VALUES
(3), -- Paul Durand
(4); -- Emma Leroy

INSERT INTO cours (idCours, nbPersMax, dureeCours, jourCours, heureCours, idMoniteur) VALUES
(101, 10, 60, '2023-10-01', '10:00:00', 3),
(102, 8, 45, '2023-10-02', '14:00:00', 4);

INSERT INTO poney (idPoney, poidMaxPoney, nomPoney) VALUES
(201, 200.0, 'Flash'),
(202, 180.0, 'Spirit');

INSERT INTO reserver (dateCours, idPoney, idCl) VALUES
('2023-10-01', 201, 1), -- Jean Dupont réserve Flash
('2023-10-02', 202, 2); -- Sophie Martin réserve Spirit
