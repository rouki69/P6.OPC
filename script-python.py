# Importer tous les objets important
import getpass
import os
import sys
from csv import reader
from datetime import date, datetime
from netmiko import ConnectHandler

# Verifier si le dossier existe sinon le créer(pour les backups).
if not os.path.exists('Backup-Configs'):
    os.makedirs('Backup-Configs')

# Format de la date et de l'heure
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H-%M")

#La banière utilisée
def banner():
    welcome = """\033[92m
======================================================
======================================================
======================================================
============SCRIPT PYTHON POUR CISCO==================
=============Projet 6 Openclassroom===================
======================================================
======================================================  
======================================================


 \033[0m"""
    return welcome


# Initialiser la connection
def get_connection():
    device = {
        'device_type': 'cisco_ios',
        'host': input("\nHost: "),
        'username': input("Utilisateur: "),
        'password': getpass.getpass("Mot de passe: "),
        'secret': getpass.getpass("Mot de passe Secret: "),
    }
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        print(f"\nVous êtes bien connecté à {device['host']}")
        print("-------------------------------------------------\n")
        return net_connect  # On retourne la connexion.
    except:
        # Message d'erreur si la connection est impossible avec l'appareil
        print(f"\nImpossible de se connecter à {device['host']}. Vérifier que les identifiants saisis sont valides.")


# Les informations necessaire pour se connecter
def get_manuel_config():
    net_connect = get_connection()
    # Recuperation de la configuration actuelle
    output = net_connect.send_command("show running-config")
    # Recuperation du nom de l'appareil.
    hostname = net_connect.send_command("show run | in hostname")
    hostname = hostname.split()
    hostname = hostname[1]
    # Creation du fichier avec le nom la date et l'heure.
    fileName = hostname + "_" + dt_string
    # Creation du fichier texte dans le dossier backup config avec le nom la date et l'heure.
    backupFile = open("Backup-Configs/" + fileName + ".txt", "w+")
    backupFile.write(output)
    print("\nBackup creer dans " + fileName + ".txt!")
    net_connect.disconnect()


# Permet de faire le backup en prenant les informations directement du fichier CSV.
def get_saved_config(host, username, password, enable_secret):
    device = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    # Connexion avec l'appareil
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        print(f"\nVous êtes bien connecté à {device['host']}")
        # Continue le code si la connection est établie
        print("-------------------------------------------------\n") \
            # Message d'erreur si la connection est impossible avec l'appareil
    except:
        print(f"\nImpossible de se connecter à {device['host']}. Vérifier que les identifiants saisis sont valides.")
        exit()
    # Recuperation de la configuration actuelle
    output = net_connect.send_command("show running-config")
    # Recuperation du nom de l'appareil.
    hostname = net_connect.send_command("show run | in hostname")
    hostname = hostname.split()
    hostname = hostname[1]
    # Creation du fichier avec le nom la date et l'heure.
    fileName = hostname + "_" + dt_string
    # Creation du fichier texte dans le dossier backup config avec le nom la date et l'heure.
    backupFile = open("Backup-Configs/" + fileName + ".txt", "w+")
    backupFile.write(output)
    print("Backup creer dans " + fileName + ".txt!")
    net_connect.disconnect()


# Recuper le fichier CSV et recuperer les informations dedans.
def csv_option():
    csv_name = input("\nQuel est le nom du fichier CSV: ")
    with open(csv_name, 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            get_saved_config(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])


# Changer la passerelle par défaut
def change_gateway():
    net_connect = get_connection()
    print('Entrer la nouvelle passerelle :')
    new_gateway = input()
    net_connect.send_config_set("ip default-gateway {0} ".format(new_gateway))
    result = net_connect.send_command("show ip default-gateway")
    print(f"La nouvelle passerelle par défaut est: {result}")
    net_connect.send_command("wr")
    net_connect.disconnect()


# Faire un show route
def show_route():
    net_connect = get_connection()
    result = net_connect.send_command("show ip route")
    print(f"\n{result}")
    net_connect.disconnect()


# Montrer les ip associés aux interfaces
def show_int_ip():
    net_connect = get_connection()
    result = net_connect.send_command("show ip interface brief")
    print(f"\n{result}")
    net_connect.disconnect()


# Montrer la version d'IOS
def get_version():
    net_connect = get_connection()
    version = net_connect.send_command("show version | in IOS")
    print(f"\n{version}")
    net_connect.disconnect()


# Montrer la table ARP
def show_arp():
    net_connect = get_connection()
    output = net_connect.send_command("show arp")
    print(f"\n{output}")
    net_connect.disconnect()


# Ajouter un utilisateur
def add_user():
    net_connect = get_connection()
    result = net_connect.send_command("show run | inc username ")
    username = input("\nChoisissez un nom d'utilisateur: ")
    if username in result:
        print("\nL'utilisateur existe déjà veuillez réessayer")
        exit()
    else:
        password = getpass.getpass("Choisissez un mot de passe: ")
        print(f"\nCréation de l'utilisateur {username}...")
    net_connect.config_mode()
    result = net_connect.send_command(f"username {username} password {password}")
    print(f"\n{username} à bien été créé\n")
    net_connect.exit_config_mode()
    result = net_connect.send_command("show run | inc username ")
    print(result)
    net_connect.send_command("wr")
    net_connect.disconnect()


#Permet le changement de mot de passe
def change_enable_password():
    net_connect = get_connection()
    net_connect.config_mode()
    password = getpass.getpass("\nChoisissez un nouveau mot de passe secret: ")
    result = net_connect.send_command(f"enable secret {password}")
    print("\nLe nouveau mot de passe secret est ajouté")
    net_connect.send_command("wr")
    net_connect.disconnect()
    
#Menu pour faire les choix en boucle
def menu():
    
    USER_CHOICE ="""
1. Backup en rentrant vous même les IP.
2. Backup en recuperant les informations par le fichier CSV.
3. Changer la passerelle d'un routeur.
4. Faire un show route d'un routeur
5. Récuperer les IP des interfaces.
6. Connaitre la version d'IOS.
7. Voir la table ARP.
8. Ajouter un utilisateur.
9. Changer le mot de passe secret.
0. Quitter le script.

Merci de choisir une option: """


#Les différents choix disponibles
    choice = input(USER_CHOICE)

    while True:
        if choice == "1":
            # Combien d'appareil l'utilisateur veut selectionner.
            how_many = input("\nCombien d'appareil voulez vous selectionner: ")
            how_many = int(how_many)
            i = how_many
            while i >= 1:
                get_manuel_config()
                i -= 1
        elif choice == "2":
            csv_option()
        elif choice == "3":
            change_gateway()
        elif choice == "4":
            show_route()
        elif choice == "5":
            show_int_ip()
        elif choice == "6":
            get_version()
        elif choice == "7":
            show_arp()
        elif choice == "8":
            add_user()
        elif choice == "9":
            change_enable_password()
        elif choice == "0":
            sys.exit("Merci d'avoir utilisé le script. À bientôt.")
        else:
            print("Merci de choisir une commande valide")
        choice = input(USER_CHOICE)

#afficher la bannière
if __name__ == "__main__":

    print(banner() + """\033[96m """)
    menu()
