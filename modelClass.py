'''
modelClass - Fait le lien avec la BDD

Etat_dossier : 1 (envoyé) 2 (en cours) 3 (fini)

'''
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
        for user in self.session.query(Dmpcpersonnelsante).filter_by(PERSONNELSANTE_PRENOM=name,PERSONNELSANTE_MDP=password):
            if user.PERSONNELSANTE_MDP == password:
                result['auth'] = 'true'
                result['medicID'] = user.PERSONNELSANTE_ID
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
        for user in self.session.query(Dmpcpersonnelsante).filter_by(PERSONNELSANTE_PRENOM=name):
            data['name'] = user.PERSONNELSANTE_NOM
            data['lastname'] = user.PERSONNELSANTE_PRENOM
            data['id'] = user.PERSONNELSANTE_ID
            data['telephone'] = user.PERSONNELSANTE_TELEPHONE
            for speciality in self.session.query(Specialite).filter_by(SPECIALITE_ID=user.SPECIALITE_ID):
                data['specialite'] = speciality.SPECIALITE_NOM
        return json.dumps(data)

    def getPatients(self, medic_id):
        patientList = []
        for patient in self.session.query(Dmpcpatient).filter_by(PERSONNELSANTE_ID=medic_id):
            tempPatient = {}
            tempPatient['patient_id'] = patient.SSN_ID
            tempPatient['medic_id'] = patient.PERSONNELSANTE_ID
            tempPatient['patient_name'] = patient.PATIENT_NOM
            tempPatient['patient_lastname'] = patient.PATIENT_PRENOM
            tempPatient['patient_birth'] = patient.PATIENT_DATENAISSANCE
            tempPatient['patient_sexe'] = patient.PATIENT_DMPCSEXE
            patientList.append(tempPatient)
        return json.dumps(patientList)

    def getResultat(self, dmp_document_id):
        folderList = []
        for folder in self.session.query(Resultat).filter_by(DMPCDOCUMENT_ID=dmp_document_id):
            tempFolder = {}
            tempFolder['folder_id'] = folder.CONSULTATION_ID
            for consult in self.session.query(Consultation).filter_by(CONSULTATION_ID=folder.CONSULTATION_ID):
                tempFolder['consult_id'] = consult.CONSULTATION_ID
                tempFolder['consult_traitement'] = consult.TRAITEMENT
            for exam in self.session.query(Examan).filter_by(EXAMEN_ID=folder.EXAMEN_ID):
                tempFolder['medic_id'] = exam.PERSONNELSANTE_ID
                tempFolder['examen_name'] = exam.EXAMEN_NOM
            tempFolder['image_name'] = folder.IMAGE_NOM
            tempFolder['image_path'] = folder.IMAGE_PATH
            folderList.append(tempFolder)
        return json.dumps(folderList)

    def getConsults(self, patient_id):
        consultList = []
        for consult in self.session.query(Consultation).filter_by(SSN_ID=patient_id):
            tempConsult = {}
            tempConsult['consult_id'] = consult.CONSULTATION_ID
            tempConsult['patient_id'] = consult.SSN_ID
            tempConsult['traitement'] = consult.TRAITEMENT
            tempConsult['historique'] = consult.HISTORIQUE
            consultList.append(tempConsult)
        return json.dumps(consultList)

    def getExamens(self, medic_id):
        examenList = []
        for exam in self.session.query(Examan).filter_by(PERSONNELSANTE_ID=medic_id):
            tempExam = {}
            tempExam['examen_id'] = exam.EXAMEN_ID
            tempExam['medecin_id'] = exam.PERSONNELSANTE_ID
            tempExam['examen_nom'] = exam.EXAMEN_NOM
            examenList.append(tempExam)
        return json.dumps(examenList)

    def getAvis(self, consult_id):
        avis = []
        for avi in self.session.query(Avi).filter_by(CONSULTATION_ID=consult_id):
            tempAvis = {}
            tempAvis['avis_id'] = avi.DMPCSUBMISSION_ID
            tempAvis['consult_id'] = avi.CONSULTATION_ID
            tempAvis['avis'] = avi.AVIS
            avis.append(tempAvis)
        return json.dumps(avis)

    '''
        Setter of the webservice
        ========================
    '''

    def createMedic(self, name, lastname, password, specialite):
        new_medic = Dmpcpersonnelsante(PERSONNELSANTE_NOM=name,PERSONNELSANTE_PRENOM=lastname,PERSONNELSANTE_PASSWORD=password,SPECIALITE_ID=specialite)
        self.session.add(new_medic)
        self.session.commit()

    def createPatient(self, ssn_id, medic_id, name, last_name, age, gender):
        new_patient = Dmpcpatient(SSN_ID=ssn_id,PERSONNELSANTE_ID=medic_id,PATIENT_NOM=name,PATIENT_PRENOM=last_name,PATIENT_AGE=age,PATIENT_GENRE=gender)
        self.session.add(new_patient)
        self.session.commit()

    def createExamen(self, medic_id, examen_name):
        new_examen = Resultat(PERSONNELSANTE_ID=medic_id,EXAMEN_NOM=examen_name)
        self.session.add(new_examen)
        self.session.commit()

    def createConsultation(self, patient_id, tratement, histo):
        new_consult = Consultation(SSN_ID=patient_id,TRAITEMENT=tratement,HISTORIQUE=histo)
        self.session.add(new_consult)
        self.session.commit()

    def createResultat(self, consult_id, examen_id, image_nom, image_path):
        new_folder = Resultat(CONSULTATION_ID=consult_id,EXAMEN_ID=examen_id,IMAGE_NOM=image_nom,IMAGE_PATH=image_path)
        self.session.add(new_folder)
        self.session.commit()