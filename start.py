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

    @cherrypy.expose
    def createMedic(self, name, password, genre, addr, spe):
        model = ModelClass()
        model.createMedic(name, password, genre, addr, spe)
        return "Creating user oK : "+str(model.listMedic())

    @cherrypy.expose
    def listMedic(self):
        model = ModelClass()
        return str(model.listMedic())

    @cherrypy.expose
    def listFolder(self, medic):
        model = ModelClass()
        return str(model.listDossier(medic))

    @cherrypy.expose
    def createFolder(self, patient, medecin, sexe, pat, avisM, avisRef, etat):
        model = ModelClass()
        model.createDossier(patient, medecin, sexe, pat, avisM, avisRef, etat)
        return "folder created"

    @cherrypy.expose
    def auth(self, name, password):
        model = ModelClass()
        return str(model.authMedic(name, password))

    @cherrypy.expose
    def debug(self):
        model = ModelClass()
        data = "('loule', 'loule', 'F', 'sdfsdf', 'dsf')"
        return str(model.encodingJsonResult(table="medics_account", data=data))

    @cherrypy.expose
    def index(self):
        return "Teleconsult-Server v0.1"
    index.exposed = True


cherrypy.quickstart(Starter())