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
from modelClass import ModelClass

class Starter(object):

    def __init__(self):
        model = ModelClass()


    '''
    Medical part
    ============
    Create medic and list all medics
    '''
    @cherrypy.expose
    def createMedic(self, name, lastname, password, genre, addr, spe):
        model = ModelClass()
        model.createMedic(name, lastname, password, genre, addr, spe)
        return "Creating user oK : "

    @cherrypy.expose
    def createFolder(self, status, consultID, medicID, patientID, examenID, imgName, imgPWD):
        model = ModelClass()
        model.createFolder(status=status,consult_id=consultID,medic_id=medicID,patient_id=patientID,examen_id=examenID,image_name=imgName,image_path=imgPWD)
        return "Creating folder OK : "

    @cherrypy.expose
    def createExamen(self, medicID, examenName):
        model = ModelClass()
        model.createExamen(medic_id=medicID,examen_name=examenName)
        return "Creating examen OK : "

    @cherrypy.expose
    def createConsult(self, patientID, traitement, histo):
        model = ModelClass()
        model.createConsultation(patient_id=patientID,tratement=traitement,histo=histo)
        return "Creating consult OK : "

    @cherrypy.expose
    def auth(self, name, password):
        model = ModelClass()
        return str(model.authMedic(name, password))

    @cherrypy.expose
    def getMedicInfo(self, name):
        model = ModelClass()
        return str("["+model.getMedic(name)+"]")

    @cherrypy.expose
    def getFolders(self, medicID):
        model = ModelClass()
        return str(model.getFolders(medic_id=medicID))

    @cherrypy.expose
    def getExams(self, medicID):
        model = ModelClass()
        return str(model.getExamens(medic_id=medicID))

    @cherrypy.expose
    def getConsults(self, patientID):
        model = ModelClass()
        return str(model.getConsults(patient_id=patientID))

    @cherrypy.expose
    def getPatients(self, medicID):
        model = ModelClass()
        return str(model.getPatients(medic_id=medicID))

    @cherrypy.expose
    def debug(self):
        model = ModelClass()
        data = "('loule', 'loule', 'F', 'sdfsdf', 'dsf')"
        return str(model.encodingJsonResult(table="medics_account", data=data))

    '''Adding uploading function'''
    @cherrypy.expose
    def uploadImage(self, putFile, fileId):
        out = open(fileId, 'wb')
        size = 0
        while True:
            data = putFile.file.read(8192)
            if not data:
                break
            size += len(data)
            out.write(data)

    @cherrypy.expose
    def index(self):
        return "Teleconsult-Server v0.1"
    index.exposed = True

cherrypy.config.update(
    {'server.socket_host': '0.0.0.0'} )
cherrypy.quickstart(Starter())