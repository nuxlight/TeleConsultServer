# Teleconsult-Server (Webservice de test)

## Utilisation :

Authentification du medecin :
http://127.0.0.1:8080/auth?name=Lisa&password=simpsons
Création d'un medecin medic :
http://127.0.0.1:8080/createMedic?name=Lisa&password=simpsons&genre=F&addr=evergreen&spe=dermato
Listage des Medecins :
http://127.0.0.1:8080/listMedic
Création d'un dossier :
http://127.0.0.1:8080/createFolder?patient=John&medecin=Lisa&sexe=M&pat=eczema&avisM=&avisRef=&etat=1
Listage des dossiers :
http://127.0.0.1:8080/listFolder?medic=Lisa