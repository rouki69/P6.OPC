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
    
    def banner():
        welcome = """\033[92m
    ======================================================
    ======================================================
    ============BIENVENUE PROJET 6 MR REMI================
    =============SCRIPT PYTHON POUR CISCO=================
    ===============POUR OPENCLASSROOM=====================	
    ======================================================
    ======================================================
    
     \033[0m"""
        return welcome
    
    # Les informations necessaire pour se connecter
    def get_saved_config(host, username, password, enable_secret):
        cisco_ios = {
            'device_type': 'cisco_ios',
            'host': host,
            'username': username,
            'password': password,
            'secret': enable_secret,
        }
        # Connexion avec l'appareil
        net_connect = ConnectHandler(**cisco_ios)
        net_connect.enable()
        # Recuperation de la configuration actuelle
        output = net_connect.send_command("show running-config")
        #Recuperation du nom de l'appareil.
        hostname = net_connect.send_command("show run | in hostname")
        hostname = hostname.split()
        hostname = hostname[1]
        # Creation du fichier avec le nom la date et l'heure.
        fileName = hostname + "_" + dt_string
        # Creation du fichier texte dans le dossier backup config avec le nom la date et l'heure.
        backupFile = open("Backup-Configs/" + fileName + ".txt", "w+")
        backupFile.write(output)
        print("Backup creer dans " + fileName + ".txt!")
    
    #Permettre le changement de la passerelle par défaut    
    def get_gateway(host, username, password, enable_secret):    
        cisco_ios = {
            'device_type': 'cisco_ios',
            'host': host,
            'username': username,
            'password': password,
            'secret': enable_secret,
        }
        # Connexion avec l'appareil
        net_connect = ConnectHandler(**cisco_ios)
        net_connect.enable()
        print('\nEntrer la nouvelle passerelle :')
        new_gateway = input()
        result = net_connect.send_config_set("ip default-gateway {0} ".format(new_gateway))
        print(result)
        
        
    # Demander l'adresse ip, le nom d'utilisateur, le mot de passe et le mot de passe secret.
    def manual_option():
        host = input("\nIP: ")
        username = input("Utilisateur: ")
        password = getpass.getpass("Mot de Passe: ")
        enable_secret = getpass.getpass("Mot de passe secret: ")
        get_saved_config(host, username, password, enable_secret)
    
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
    
    #Affichage de la table de routage des routeurs
    def change_gateway():
        host = input("\nIP: ")
        username = input("Utilisateur ")
        password = getpass.getpass("Mot de passe: ")
        enable_secret = getpass.getpass("Mot de passe secret: ")
        get_gateway(host, username, password, enable_secret)
        
    #Faire un show route
    def get_show_route(host, username, password, enable_secret):    
        cisco_ios = {
            'device_type': 'cisco_ios',
            'host': host,
            'username': username,
            'password': password,
            'secret': enable_secret,
        }
        # Connexion avec l'appareil
        net_connect = ConnectHandler(**cisco_ios)
        net_connect.enable()
        result = net_connect.send_command("show ip route")
        print(result)
    
        
    #Recuperer information pour show route
    def show_route():
        host = input("\nIP: ")
        username = input("Utilisateur ")
        password = getpass.getpass("Mot de passe: ")
        enable_secret = getpass.getpass("Mot de passe secret: ")
        get_show_route(host, username, password, enable_secret)
        
        
    #Connaitre l'adresse ip des interfaces
    def get_int_ip(host, username, password, enable_secret):    
        cisco_ios = {
            'device_type': 'cisco_ios',
            'host': host,
            'username': username,
            'password': password,
            'secret': enable_secret,
        }
        # Connexion avec l'appareil
        net_connect = ConnectHandler(**cisco_ios)
        net_connect.enable()
        result = net_connect.send_command("show ip interface brief")
        print(result)
    
        
    #Donnee pour interface IP
    def show_int_ip():
        host = input("\nIP: ")
        username = input("Utilisateur ")
        password = getpass.getpass("Mot de passe: ")
        enable_secret = getpass.getpass("Mot de passe secret: ")
        get_int_ip(host, username, password, enable_secret)    
       
        
        
    print (banner() + """\033[96m """)
    # Demander a l utilisateur les options qu ils souhaitent
    print("\n1. Backup en rentrant vous même les IP.")
    print("2. Backup en recuperant les informations par le fichier CSV.")
    print("3. Changer la passerelle d'un routeur.")
    print("4. Faire un show route d'un routeur")
    print("5. Récuperer les IP des interfaces.")
    print("0. Quitter le script.")
    
    choice = input("\nMerci de choisir une option: ")
    # Pour lancer les differentes options.
    
    if choice == "1":
        #Combien d'appareil l'utilisateur veut selectionner.
        how_many = input("Combien d'appareil voulez vous selectionner: ")
        how_many = int(how_many)
        i = how_many
        while i >= 1:
            manual_option()
            i = i - 1
    elif choice == "2":
        # Utiliser l'option CSV.
         csv_option()
    elif choice == "3":
    #Choix pour changer la passerelle
         change_gateway()  
    elif choice == "4":
         show_route() 
    #Choix pour faire un show route
    elif choice == "5":
         show_int_ip()
    elif choice == "0":
         sys.exit("\nMerci d'avoir utilisé le script au revoir\n")
    else :
         sys.exit("\n --Merci de séléctionner une option val
