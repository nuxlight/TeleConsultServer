'''
 _____    _       ____                      _ _   ____
|_   _|__| | ___ / ___|___  _ __  ___ _   _| | |_/ ___|  ___ _ ____   _____ _ __
  | |/ _ \ |/ _ \ |   / _ \| '_ \/ __| | | | | __\___ \ / _ \ '__\ \ / / _ \ '__|
  | |  __/ |  __/ |__| (_) | | | \__ \ |_| | | |_ ___) |  __/ |   \ V /  __/ |
  |_|\___|_|\___|\____\___/|_| |_|___/\__,_|_|\__|____/ \___|_|    \_/ \___|_|

  ====================================================================

  Partie serveur du projet, ce petit programme fonctionne comme un web service.

'''
import cherrypy
import logging as Log
from modelClass import ModelClass

class Starter(object):

    def __init__(self):
        model = ModelClass()

    # -------------------
    # Medic part
    # -------------------
    @cherrypy.expose
    def createMedic(self, name, lastname, password, genre, addr, spe):
        model = ModelClass()
        model.createMedic(name, lastname, password, genre, addr, spe)
        return "Creating medic OK"

    @cherrypy.expose
    def auth(self, name, password):
        model = ModelClass()
        return str(model.authMedic(name, password))

    # -------------------
    # Examen part
    # -------------------
    @cherrypy.expose
    def createExamen(self, medicID, examenName):
        model = ModelClass()
        model.createExamen(medic_id=medicID,examen_name=examenName)
        return "Creating examen OK"

    @cherrypy.expose
    def getExams(self, medicID):
        model = ModelClass()
        return str(model.getExamens(medic_id=medicID))

    # -------------------
    # Consultation part
    # -------------------
    @cherrypy.expose
    def createConsult(self, patientID, date, traitement, histo):
        model = ModelClass()
        model.createConsultation(patient_id=patientID,date=date,tratement=traitement,histo=histo)
        return "Creating consult OK"

    @cherrypy.expose
    def getConsult(self, patientID):
        model = ModelClass()
        return str(model.getConsults(patient_id=patientID))

    # -------------------
    # Resultat part
    # -------------------
    @cherrypy.expose
    def createResult(self, consultID, examenID, imageName, imagePath, heartEntry):
        model = ModelClass()
        model.createResultat(consult_id=consultID,examen_id=examenID,image_nom=imageName,image_path=imagePath,hearthMeasure=heartEntry)
        return "Creating result OK"

    @cherrypy.expose
    def getResult(self, resultID):
        model = ModelClass()
        return str(model.getResultat(dmp_document_id=resultID))

    # ------------------------------------- #
    # Debuging arena                        #
    # ------------------------------------- #
    @cherrypy.expose
    def getMedicInfo(self, name):
        model = ModelClass()
        return str("["+model.getMedic(name)+"]")

    @cherrypy.expose
    def getPatients(self, medicID):
        model = ModelClass()
        return str(model.getPatients(medic_id=medicID))

    @cherrypy.expose
    def debug(self):
        model = ModelClass()
        data = "('loule', 'loule', 'F', 'sdfsdf', 'dsf')"
        return str(model.encodingJsonResult(table="medics_account", data=data))

    @cherrypy.expose
    def uploadImage(self, fileImg):
        path = "./images/"+str(fileImg.filename)
        out = open(path, 'wb')
        size = 0
        while True:
            data = fileImg.file.read(8192)
            if not data:
                break
            size += len(data)
            out.write(data)
        return "Image added file name :"

    @cherrypy.expose
    def index(self):
        return "Teleconsult-Server v0.1"
    index.exposed = True

Log.basicConfig(filename='teleconsult.log',level=Log.DEBUG)
# Start webservice
cherrypy.config.update(
    {'server.socket_host': '0.0.0.0', 'server.socket_port': 7777})
cherrypy.quickstart(Starter())