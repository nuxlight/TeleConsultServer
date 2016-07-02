'''
modelClass - Fait le lien avec la BDD

@Thibaud : J'ai fait que deux table pour l'instant

CREATE TABLE IF NOT EXISTS medics_account(
    name VARCAHR(25),
    genre VARCHAR(1),
    adresse VARCHAR(50),
    specialite VARCHAR(25)
);

CREATE TABLE IF NOT EXISTS patients_folder (
    patient VARCHAR(25),
    sexe VARCHAR(1),
    pathologie VARCHAR(25),
    avis_medecin VARCHAR(200),
    avis_ref VARCHAR(200),
    etat_dossier INT(3)
);

Etat_dossier : 1 (envoyé) 2 (en cours) 3 (fini)

'''
import sqlite3
import collections
import json

from docutils.parsers import null


class ModelClass():
    def __init__(self):
        print("Start database")
        self.con = sqlite3.connect('teleconsult.db')
        self.cursor = self.con.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS medics_account(
                name VARCHAR(25),
                password VARCHAR(25),
                genre VARCHAR(1),
                adresse VARCHAR(50),
                specialite VARCHAR(25)
            );''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS patients_folder (
                patient VARCHAR(25),
                medecin VARCHAR(25),
                sexe VARCHAR(1),
                pathologie VARCHAR(25),
                avis_medecin VARCHAR(200),
                avis_ref VARCHAR(200),
                etat_dossier INT(3)
            );''')

    def createMedic(self, name, password, genre, addresse, spe):
        query = "INSERT INTO medics_account VALUES ('"+name+"','"+password+"','"+genre+"','"+addresse+"','"+spe+"')"
        self.con.execute(query)
        self.con.commit()

    def authMedic(self, name, password):
        query = "SELECT * FROM medics_account WHERE name LIKE '"+name+"' AND password LIKE '"+password+"'"
        result = self.cursor.execute(query)
        row = result.fetchone()
        print(str(row))
        if str(row) != "None":
            return 'true'
        else:
            return 'false'

    def listDossier(self, medic):
        query = "SELECT * FROM patients_folder WHERE medecin LIKE '"+medic+"'"
        result = self.cursor.execute(query)
        return self.encodingJsonResult('patients_folder',result.fetchall())

    def createDossier(self, patient, medecin, sexe, pathologie, avis_medecin, avis_ref, etat_dossier):
        query = "INSERT INTO patients_folder VALUES ('" + patient + "','" + medecin + "','" + sexe + "','" + pathologie + "','" + avis_medecin + "','" + avis_ref + "','" + etat_dossier + "')"
        self.con.execute(query)
        self.con.commit()

    def listMedic(self):
        result = self.cursor.execute("SELECT * FROM medics_account")
        return self.encodingJsonResult('medics_account', result.fetchall())

    def encodingJsonResult(self, table, data):
        query = "PRAGMA table_info("+table+");"
        result = self.cursor.execute(query)
        result = result.fetchall()
        finalArray = []
        for entry in data:
            print(entry)
            index = 0
            d = collections.OrderedDict()
            for row in result:
                print(entry[index])
                d[row[1]] = entry[index]
                index = index+1
            finalArray.append(d)
        return json.dumps(finalArray)