# Projet 6 pour Openclassroom


# __Script Python pour routeur cisco__


## Description

J'ai créé ce script en python pour pouvoir automatiser certaines tâches avec des routeurs en connexion SSH.

Les configuration Cisco de votre appareil seront enregistrées dans un dossier avec le nom d'hôte, la date et l'heure. Vous avez la possibilité de tout importer à partir d'un fichier CSV ou de lui donner manuellement l'adresse IP, le nom d'utilisateur, le mot de passe secret de chaque hote. 

Voici les possibilités possibles avec ce script:
* Faire un back-up en tapant directement les informations manuellement ou depuis un fichier CSV.
* Changer la passerelle d'un routeur.
* Voir les adresses IP des interfaces.
* Connaître la version d'IOS utilisé. 
* Voir la table ARP.
* Ajouter un utilisateur sur le routeur.
* Changer le mot de passe secret (le mot de passe changé sera le secret et non le enable il sera stocké sous forme de hashage MD5)


## Pré-requis
Il est nécessaire d'avoir un accès SSH sur les routeurs ciblés, ainsi que d'un utilisateur sur chaque routeur.

## Installation
`pip3 install -r requirements.txt`


## Configuration

Si vous souhaite utiliser un fichier CSV pour l'utiliser dans le script il suffit de suivre les indications dedans.
Le dossier pour les back-up sera automatiquement créé ou se situe le script.

![Screenshot](images/CSV.PNG)

## Démarrage

Dans l'invite de commande il suffit d'executer le "script-python.py"

Exemple avec Ubuntu : $ python3 run.py 

![Screenshot](images/Demarrage.PNG)

## Utilisation

Depuis le menu, il suffit de selectionner l'option qui vous interesse.

Si vous choisissez l'option CSV, vous aurez besoin dudit fichier CSV dans le même répertoire que le script Python. Il copiera la configuration enregistrée dans un dossier nommé Backup-Configs dans le même répertoire du fichier python. Le nom du fichier de configuration sera le nom d'hôte, la date et l'heure du périphérique Cisco.
## Laboratoire de test

Les test ont étés efféctues avec [GNS3](https://gns3.com/) avec plusieurs routeurs et une machine sous Ubuntu 20.04.

![Screenshot](images/GNS3-P6.PNG)


## Exemples
Pour le backup il est possible de récuperer le fichier CSV ou vous aurez au préalable rempli avec les informations concernant les routeurs.

![Screenshot](images/exemple-backup.PNG)

Pour faire un show interface sur le routeur souhaité :
![Screenshot](images/exemple-ip.PNG)



