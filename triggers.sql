-- Contrainte 1: Un cours ne peut pas dépasser 10 personnes
DELIMITER |
CREATE OR REPLACE TRIGGER checkInsertNbPersMax 
BEFORE INSERT ON RESERVER FOR EACH ROW
BEGIN
    DECLARE nbPers INT;
    DECLARE mes VARCHAR(200);

    SELECT COUNT(*) INTO nbPers
    FROM RESERVER
    WHERE idCours = NEW.idCours AND dateCours = NEW.dateCours;

    IF nbPers >= 10 THEN
        mes = "Le cours ne peut pas dépasser 10 personnes";
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = mes;
    END IF;
END |
DELIMITER;

DELIMITER |
CREATE OR REPLACE TRIGGER checkUpdateNbPersMax
BEFORE UPDATE ON RESERVER FOR EACH ROW
BEGIN
    DECLARE nbPers INT;
    DECLARE mes VARCHAR(200);

    SELECT COUNT(*) INTO nbPers
    FROM RESERVER
    WHERE idCours = NEW.idCours AND dateCours = NEW.dateCours;

    IF nbPers >= 10 THEN
        mes = "Le cours ne peut pas dépasser 10 personnes";
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = mes;
    END IF;
END |
DELIMITER;


--Contrainte 2: Un poney ne peut pas être utilisé après un cours sans 1h de pause
DELIMITER |
CREATE OR REPLACE TRIGGER checkInsertPoneyPause 
BEFORE INSERT ON RESERVER FOR EACH ROW
BEGIN
    DECLARE heureCours TIME;
    DECLARE heureFinDeCours TIME;
    DECLARE heureDernierCours TIME;
    DECLARE dureeDernierCours INT;
    DECLARE mes VARCHAR(200);

    SELECT heureCours INTO heureCours
    FROM COURS
    WHERE idCours = NEW.idCours;

    SELECT dureeCours INTO dureeDernierCours
    FROM COURS
    WHERE idCours = NEW.idCours;

    SET heureFinDeCours = ADDTIME(heureCours, CONCAT(dureeDernierCours, ':00:00'));

    SELECT heureCours INTO heureDernierCours
    FROM RESERVER NATURAL JOIN COURS
    WHERE idPoney = NEW.idPoney
      AND dateCours = NEW.dateCours
    ORDER BY heureCours DESC
    LIMIT 1;

    IF heureDernierCours IS NOT NULL AND ADDTIME(heureDernierCours, CONCAT(dureeDernierCours, ':00:00')) > SUBTIME(heureCours, '01:00:00') THEN
        SET mes = "Le poney ne peut pas être utilisé après un cours sans 1h de pause.";
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = mes;
    END IF;
END |
DELIMITER;


DELIMITER |
CREATE OR REPLACE TRIGGER checkUpdatePoneyPause 
BEFORE UPDATE ON RESERVER FOR EACH ROW
BEGIN
    DECLARE heureCours TIME;
    DECLARE heureFinDeCours TIME;
    DECLARE heureDernierCours TIME;
    DECLARE dureeDernierCours INT;
    DECLARE mes VARCHAR(200);

    SELECT heureCours INTO heureCours
    FROM COURS
    WHERE idCours = NEW.idCours;

    SELECT dureeCours INTO dureeDernierCours
    FROM COURS
    WHERE idCours = NEW.idCours;

    SET heureFinDeCours = ADDTIME(heureCours, CONCAT(dureeDernierCours, ':00:00'));

    SELECT heureCours INTO heureDernierCours
    FROM RESERVER NATURAL JOIN COURS
    WHERE idPoney = NEW.idPoney
      AND dateCours = NEW.dateCours
    ORDER BY heureCours DESC
    LIMIT 1;

    IF heureDernierCours IS NOT NULL AND ADDTIME(heureDernierCours, CONCAT(dureeDernierCours, ':00:00')) > SUBTIME(heureCours, '01:00:00') THEN
        SET mes = "Le poney ne peut pas être utilisé après un cours sans 1h de pause.";
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = mes;
    END IF;
END |
DELIMITER;


--Contrainte 3: Un poney ne peut pas porter un cavalier supérieur à sa limite de poids
DELIMITER |
CREATE OR REPLACE TRIGGER checkInsertPoneyPoids
BEFORE INSERT ON RESERVER FOR EACH ROW
BEGIN
    DECLARE poidsClient FLOAT;
    DECLARE poidsMaxPoney FLOAT;
    DECLARE mes VARCHAR(200);

    SELECT poidCl INTO poidsClient
    FROM CLIENT
    WHERE idCl = NEW.idCl;

    SELECT poidMaxPoney INTO poidsMaxPoney
    FROM PONEY
    WHERE idPoney = NEW.idPoney;

    IF poidsClient > poidsMaxPoney THEN
        SET mes = "Le cavalier dépasse le poids limite du poney.";
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = mes;
    END IF;
END |
DELIMITER;

DELIMITER |
CREATE OR REPLACE TRIGGER checkUpdatePoneyPoids
BEFORE UPDATE ON RESERVER FOR EACH ROW
BEGIN
    DECLARE poidsClient FLOAT;
    DECLARE poidsMaxPoney FLOAT;
    DECLARE mes VARCHAR(200);

    SELECT poidCl INTO poidsClient
    FROM CLIENT
    WHERE idCl = NEW.idCl;

    SELECT poidMaxPoney INTO poidsMaxPoney
    FROM PONEY
    WHERE idPoney = NEW.idPoney;

    IF poidsClient > poidsMaxPoney THEN
        SET mes = "Le cavalier dépasse le poids limite du poney.";
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = mes;
    END IF;
END |
DELIMITER;


-- Contrainte 4: Un moniteur peut donner un cours particulier à un seul cavalier
DELIMITER |
CREATE OR REPLACE TRIGGER checkInsertMoniteurCoursParticulier
BEFORE INSERT ON RESERVER FOR EACH ROW
BEGIN
    DECLARE nbCoursParticulier INT;
    DECLARE mes VARCHAR(200);
    DECLARE heureCours TIME;

    SELECT heureCours INTO heureCours
    FROM COURS NATURAL JOIN COURS_REALISE
    WHERE idCours = NEW.idCours
    AND dateCours = NEW.dateCours;

    SELECT COUNT(*) INTO nbCoursParticulier
    FROM RESERVER NATURAL JOIN COURS NATURAL JOIN COURS_REALISE
    WHERE COURS.idMoniteur = (SELECT idMoniteur FROM COURS WHERE idCours = NEW.idCours)
    AND RESERVER.dateCours = NEW.dateCours
    AND RESERVER.heureCours = heureCours;

    IF nbCoursParticulier > 0 THEN
        SET mes = "Le moniteur ne peut donner qu'un cours particulier à la fois à la même heure.";
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = mes;
    END IF;
END |
DELIMITER;


DELIMITER |
CREATE OR REPLACE TRIGGER checkUpdateMoniteurCoursParticulier
BEFORE UPDATE ON RESERVER FOR EACH ROW
BEGIN
    DECLARE nbCoursParticulier INT;
    DECLARE mes VARCHAR(200);
    DECLARE heureCours TIME;

    SELECT heureCours INTO heureCours
    FROM COURS NATURAL JOIN COURS_REALISE
    WHERE idCours = NEW.idCours
    AND dateCours = NEW.dateCours;

    SELECT COUNT(*) INTO nbCoursParticulier
    FROM RESERVER NATURAL JOIN COURS NATURAL JOIN COURS_REALISE
    WHERE COURS.idMoniteur = (SELECT idMoniteur FROM COURS WHERE idCours = NEW.idCours)
    AND RESERVER.dateCours = NEW.dateCours
    AND RESERVER.heureCours = heureCours;

    IF nbCoursParticulier > 0 THEN
        SET mes = "Le moniteur ne peut donner qu'un cours particulier à la fois à la même heure.";
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = mes;
    END IF;
END |
DELIMITER;


-- Contrainte 5: Les adhérents doivent régler une cotisation annuelle pour pouvoir réserver
DELIMITER |
CREATE OR REPLACE TRIGGER checkCotisationPaye BEFORE INSERT ON RESERVER
FOR EACH ROW
BEGIN
    DECLARE cotisationReglee BOOLEAN;
    DECLARE mes VARCHAR(200);

    SELECT (dateRegCoti IS NOT NULL) INTO cotisationReglee
    FROM CLIENT
    WHERE idCl = NEW.idCl;

    IF NOT cotisationReglee THEN
        SET mes = "L'adhérent doit régler sa cotisation annuelle pour pouvoir réserver.";
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = mes;
    END IF;
END |
DELIMITER;

DELIMITER |
CREATE OR REPLACE TRIGGER checkCotisation BEFORE UPDATE ON RESERVER
FOR EACH ROW
BEGIN
    DECLARE cotisationReglee BOOLEAN;
    DECLARE mes VARCHAR(200);
    
    SELECT (dateRegCoti IS NOT NULL) INTO cotisationReglee
    FROM CLIENT
    WHERE idCl = NEW.idCl;
    
    IF NOT cotisationReglee THEN
        SET mes = "L'adhérent doit régler sa cotisation annuelle pour pouvoir réserver.";
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = mes;
    END IF;
END |
DELIMITER;