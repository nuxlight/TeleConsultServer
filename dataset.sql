-- phpMyAdmin SQL Dump
-- version 4.4.10
-- http://www.phpmyadmin.net
--
-- Client :  localhost:3306
-- Généré le :  Dim 31 Juillet 2016 à 18:26
-- Version du serveur :  5.5.42
-- Version de PHP :  7.0.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

INSERT INTO `specialite` (`SPECIALITE_ID`, `SPECIALITE_NOM`) VALUES
(1, 'Dermatologue');

INSERT INTO `medecin` (`MEDECIN_ID`, `MEDECIN_NOM`, `MEDECIN_PRENOM`, `MEDECIN_PASSWORD`, `MEDECIN_GENRE`, `MEDECIN_ADDR`, `SPECIALITE_ID`) VALUES
(1, 'Lisa', 'Simpsons', 'loule', 'F', 'Rue bidon', 1);

INSERT INTO `patient` (`SSN_ID`, `MEDECIN_ID`, `PATIENT_NOM`, `PATIENT_PRENOM`, `PATIENT_AGE`, `PATIENT_GENRE`) VALUES
('123', 1, 'Bouchard', 'John', 23, 'M');
INSERT INTO `patient` (`SSN_ID`, `MEDECIN_ID`, `PATIENT_NOM`, `PATIENT_PRENOM`, `PATIENT_AGE`, `PATIENT_GENRE`) VALUES
('1245678765', 1, 'Stone', 'Lucie', 30, 'F');

INSERT INTO `examen` (`EXAMEN_ID`, `MEDECIN_ID`, `EXAMEN_NOM`) VALUES
(1, 1, 'Curetage');
INSERT INTO `examen` (`EXAMEN_ID`, `MEDECIN_ID`, `EXAMEN_NOM`) VALUES
(2, 1, 'Palpation');

INSERT INTO `consultation` (`CONSULTATION_ID`, `SSN_ID`, `TRAITEMENT`, `HISTORIQUE`) VALUES
(1, '123', 'Medicament', 'RAS');
INSERT INTO `consultation` (`CONSULTATION_ID`, `SSN_ID`, `TRAITEMENT`, `HISTORIQUE`) VALUES
(2, '1245678765', 'Medicament', 'RAS');

INSERT INTO `dossier` (`DOSSIER_ID`, `DOSSIER_STATUS`, `CONSULTATION_ID`, `MEDECIN_ID`, `SSN_ID`, `EXAMEN_ID`, `IMAGE_NOM`, `IMAGE_PATH`) VALUES
(1, 'En cours', 1, 1, '123', 1, 'Test', '/test/img');
INSERT INTO `dossier` (`DOSSIER_ID`, `DOSSIER_STATUS`, `CONSULTATION_ID`, `MEDECIN_ID`, `SSN_ID`, `EXAMEN_ID`, `IMAGE_NOM`, `IMAGE_PATH`) VALUES
(2, 'En cours', 2, 1, '1245678765', 1, 'Test', '/test/img2');