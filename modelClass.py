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

    '''
        Getter of the webservice
        ========================
    '''

    def getMedic(self, name):
        data = {}
        for user in self.session.query(MEDECIN).filter_by(MEDECIN_NOM=name):
            data['name'] = user.MEDECIN_NOM
            data['lastname'] = user.MEDECIN_PRENOM
            data['id'] = user.MEDECIN_ID
            data['genre'] = user.MEDECIN_GENRE
            data['adresse'] = user.MEDECIN_ADDR
            for speciality in self.session.query(SPECIALITE).filter_by(SPECIALITE_ID=user.SPECIALITE_ID):
                data['specialite'] = speciality.SPECIALITE_NOM
        return json.dumps(data)

    def getPatients(self, medic_id):
        patientList = []
        for patient in self.session.query(PATIENT).filter_by(MEDECIN_ID=medic_id):
            tempPatient = {}
            tempPatient['patient_id'] = patient.SSN_ID
            tempPatient['medic_id'] = patient.MEDECIN_ID
            tempPatient['patient_name'] = patient.PATIENT_NOM
            tempPatient['patient_lastname'] = patient.PATIENT_PRENOM
            tempPatient['patient_age'] = patient.PATIENT_AGE
            tempPatient['patient_gender'] = patient.PATIENT_GENRE
            patientList.append(tempPatient)
        return json.dumps(patientList)

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

    def getConsults(self, patient_id):
        consultList = []
        for consult in self.session.query(CONSULTATION).filter_by(SSN_ID=patient_id):
            tempConsult = {}
            tempConsult['consult_id'] = consult.CONSULTATION_ID
            tempConsult['patient_id'] = consult.SSN_ID
            tempConsult['traitement'] = consult.TRAITEMENT
            tempConsult['historique'] = consult.HISTORIQUE
            consultList.append(tempConsult)
        return json.dumps(consultList)

    def getExamens(self, medic_id):
        examenList = []
        for exam in self.session.query(EXAMEN).filter_by(MEDECIN_ID=medic_id):
            tempExam = {}
            tempExam['examen_id'] = exam.EXAMEN_ID
            tempExam['medecin_id'] = exam.MEDECIN_ID
            tempExam['examen_nom'] = exam.EXAMEN_NOM
            examenList.append(tempExam)
        return json.dumps(examenList)

    def getAvis(self, consult_id):
        avis = []
        for avi in self.session.query(EXAMEN).filter_by(CONSULTATION_ID=consult_id):
            tempAvis = {}
            tempAvis['consult_id'] = avi.CONSULTATION_ID
            tempAvis['medic_id'] = avi.MEDECIN_ID
            tempAvis['avis'] = avi.AVIS
            avis.append(tempAvis)
        return json.dumps(avis)

    '''
        Setter of the webservice
        ========================
    '''

    def createMedic(self, name, lastname, password, genre, addr, spe):
        new_medic = MEDECIN(MEDECIN_NOM=name,MEDECIN_PRENOM=lastname,MEDECIN_PASSWORD=password,MEDECIN_GENRE=genre,MEDECIN_ADDR=addr,SPECIALITE_ID=spe)
        self.session.add(new_medic)
        self.session.commit()

    def createPatient(self, ssn_id, medic_id, name, last_name, age, gender):
        new_patient = PATIENT(SSN_ID=ssn_id,MEDECIN_ID=medic_id,PATIENT_NOM=name,PATIENT_PRENOM=last_name,PATIENT_AGE=age,PATIENT_GENRE=gender)
        self.session.add(new_patient)
        self.session.commit()

    def createExamen(self, medic_id, examen_name):
        new_examen = EXAMEN(MEDECIN_ID=medic_id,EXAMEN_NOM=examen_name)
        self.session.add(new_examen)
        self.session.commit()

    def createConsultation(self, patient_id, tratement, histo):
        new_consult = CONSULTATION(SSN_ID=patient_id,TRAITEMENT=tratement,HISTORIQUE=histo)
        self.session.add(new_consult)
        self.session.commit()

    def createFolder(self, status, consult_id, medic_id, patient_id, examen_id, image_name, image_path):
        new_folder = DOSSIER(DOSSIER_STATUS=status, CONSULTATION_ID=consult_id, MEDECIN_ID=medic_id, SSN_ID=patient_id, EXAMEN_ID=examen_id, IMAGE_NOM=image_name, IMAGE_PATH=image_path)
        self.session.add(new_folder)
        self.session.commit()