'''
modelClass - Fait le lien avec la BDD

Etat_dossier : 1 (envoyé) 2 (en cours) 3 (fini)

'''
import collections
import json
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from orm import *


class ModelClass():
    def __init__(self):
        engine = create_engine("mysql+pymysql://root:root@localhost/teleconsult?host=localhost?port=3306")
        self.con = engine.connect()
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        print("SQLAlchemy is connected and ready to right")

    def createMedic(self, name, lastname, password, genre, addr, spe):
        new_medic = MEDECIN(MEDECIN_NOM=name,MEDECIN_PRENOM=lastname,MEDECIN_PASSWORD=password,MEDECIN_GENRE=genre,MEDECIN_ADDR=addr,SPECIALITE_ID=spe)
        self.session.add(new_medic)
        self.session.commit()

    def authMedic(self, name, password):
        result = {}
        for user in self.session.query(MEDECIN).filter_by(MEDECIN_NOM=name,MEDECIN_PASSWORD=password):
            if user.MEDECIN_PASSWORD == password:
                result['auth'] = 'true'
                result['medicID'] = user.MEDECIN_ID
                return json.dumps(result)
            else:
                result['auth'] = 'false'
                result['medicID'] = null
                return json.dumps(result)

    def getMedic(self, name):
        data = {}
        for user in self.session.query(MEDECIN).filter_by(MEDECIN_NOM=name):
            data['name'] = user.MEDECIN_NOM
            data['genre'] = user.MEDECIN_GENRE
            data['adresse'] = user.MEDECIN_ADDR
            for speciality in self.session.query(SPECIALITE).filter_by(SPECIALITE_ID=user.SPECIALITE_ID):
                data['specialite'] = speciality.SPECIALITE_NOM
        return json.dumps(data)

    def getFolders(self, medic_id):
        folderList = []
        for folder in self.session.query(DOSSIER).filter_by(MEDECIN_ID=medic_id):
            tempFolder = {}
            tempFolder['folder_id'] = folder.CONSULTATION_ID
            tempFolder['folder_status'] = folder.DOSSIER_STATUS
            for consult in self.session.query(CONSULTATION).filter_by(CONSULTATION_ID=folder.CONSULTATION_ID):
                tempFolder['consult_id'] = consult.CONSULTATION_ID
                tempFolder['traitement'] = consult.TRAITEMENT
            for patient in self.session.query(PATIENT).filter_by(SSN_ID=folder.SSN_ID):
                tempFolder['patient_name'] = patient.PATIENT_NOM
                tempFolder['patient_lastname'] = patient.PATIENT_PRENOM
                tempFolder['patient_age'] = patient.PATIENT_AGE
                tempFolder['patient_genre'] = patient.PATIENT_GENRE
            for exam in self.session.query(EXAMEN).filter_by(EXAMEN_ID=folder.EXAMEN_ID):
                tempFolder['examen_name'] = exam.EXAMEN_NOM
            folderList.append(tempFolder)
        return json.dumps(folderList)

    def listDossier(self, medic):
        query = "SELECT * FROM patients_folder WHERE medecin LIKE '"+medic+"'"
        result = self.cursor.execute(query)
        return self.encodingJsonResult('patients_folder',result.fetchall())

    def createDossier(self, patient, medecin, sexe, age, pathologie, avis_medecin, avis_ref, etat_dossier):
        query = "INSERT INTO patients_folder VALUES ('" + patient + "','" + medecin + "','" + sexe + "','" + age + "','"+ pathologie + "','" + avis_medecin + "','" + avis_ref + "','" + etat_dossier + "')"
        self.con.execute(query)
        self.con.commit()