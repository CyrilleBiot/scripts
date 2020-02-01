#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Script d'installation et de configuration du serveur de cache apt
    apt-cacher-ng soit en tant que serveur (ajout du paquet sur le système
    soit en tant que client (cration d'un fichier de proxy apt)
"""

__author__ = "Cyrille BIOT"
__copyright__ = "Copyleft"
__credits__ = "Cyrille BIOT"
__license__ = "GPL"
__version__ = "0.2.2"
__date__ = "2020/01/30"
__maintainer__ = "Cyrille BIOT"
__email__ = "cyrille@cbiot.fr"
__status__ = "Devel"

import os, re, sys, platform
import nmap, subprocess, socket



def baseDebian():
    """
    Fonction permettant de connaitre le Systeme d'exploitant faisant tourner le script
    Ou DEBIAN ou UBUNTU pour savoir si on utilise su ou sudo
    Retourne une variable de type string (admin)
    :return: admin soit 'su' soit 'sudo'
    """
    # Ubuntu ou DEBIAN
    if 'Debian' in platform.version():
        # Si DEBIAN, verif si root lance le script
        admin = 'su'
        print('Vous utilisez un système Debian (su pour adminstration).')
        if not os.geteuid() == 0:
            sys.exit("Seul le root peut lancer ce script. Nécessite privilèges administrateur")
    else:
        print('Vous utilisez un système non Debian (sudo pour adminstration).')
        admin = 'sudo'
    return admin


def installServeur(ip, port):
    """
    Fonction installant le serveur de cache apt-cacher-ng
    :param ip: IP du Serveur
    :param port: interger port ACN
    :return:
    """
    # Installation SERVEUR
    # Tester si le package apt-cacher-ng est installé ou non
    retval = subprocess.call(["which", "apt-cacher-ng"])
    if retval != 0:
        print("Le package apt-cacher-ng n'est pas intallé. Installation...")

        # Paramètres de l'install
        cmdInstall = ['apt-get', 'install', 'apt-cacher-ng', '-y']
        cmdUpdate = ['apt-get', 'update']
        # Debian, Ubuntu
        admin = baseDebian()

        # Adaptation système Ubuntu
        if admin == 'sudo':
            cmdInstall.insert(0, 'sudo')
            cmdUpdate.insert(0, 'sudo')

        # On installe le paquet
        subprocess.run(cmdInstall)
        subprocess.run(cmdUpdate)
    else:
        print('Le package apt-cacher-ng est déjà présent sur votre système.')
        sys.exit()

    # Affichage Informations
    print("===============================================")
    print("Le serveur de cache est dès lors opérationnel")
    print("Le port d'écoute est : {}".format(portACN))
    print("Page d'aministration : http://{}:{}/acng-report.html".format(ipServeur, portACN))
    print("Notez bien l'ip de votre serveur, elle vous sera indispensable pour la configuration des clients.")
    print("L'IP du serveur est : {} ".format(ipServeur))
    print("Indispensable : cette IP doit être FIXE (réglage sur votre BOX ou serveur DHCP).")


def installClient(ipServeur,portACN):
    """
    Fonction installant un fichier de configuration apt pour les postes clients
    Créer un fichier dans /etc/apt/apt.conf.d/ ayant pour nom 00aptproxyANC
    :param ipServeur:  ip du serveur ACN
    :param portACN: port d'écoute du serveur ACN
    :return:
    """
    print("Installation client.")
    # Reste à insérer l'ip et à le coller au bo n endroit
    msgApt = 'Acquire::http::Proxy "http://' + ipServeur + ':' + str(portACN) + '";\n'
    print(msgApt)
    dirInstall = '/etc/apt/apt.conf.d/'
    fileName = '00aptproxyANC'
    fileLocInstall = dirInstall + fileName
    fichier = open(fileLocInstall, "w")
    fichier.write(msgApt)
    fichier.close()


def ipRecuperation():
    """
    Fonction récupérant l'adresse IPv 4 de la machine
    :return: l'ip de la machine lançant ce script
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]


def ipTest(ip):
    """
    Fonction testant la validité d'une adresse IPv4
    :param ip: ip à tester
    :return: True si IP valide, False sinon
    """
    reg = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
    if re.match(reg, ip):
        return True
    else:
        return False


def clientServeur():
    """
    Fonction déterminant s'il s'agit d'une installation de type Serveur ou Client
    :return: Retourne une variable string soit client soit serveur
    """
    while True:
        try:
            choixInstall = input("Type d'installation (client/serveur) : ")
            if choixInstall.lower() in ['client', 'serveur']:
                print('Installation de type {}'.format(choixInstall))
                break
            else:
                print('Préciser : client OU serveur.')
                print('ATTENTION A LA CASSE. Pas de majuscule.')
        except ValueError:
            print("Oops!  Réponse incorrecte... Réessayer...")
    return choixInstall

def portStatus(ip, port):
    """
    Fonction de scanne d'un port d'une machine en fonction de son IP
    :param ip:
    :param port:
    :return: Retourne True si port ouvert ou False si port fermé
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False

def chercherServeurACN(ip,port):
    """
    Fonction recherchant
    :param ip: IP du client lançant le scan, permet de trouver un motif réseau
    :param port: port à scanner (port ACN)
    :return: retourne une liste contenant les IP possibles des machines ayant port spécifié ouvert
    """
    ipModele = ''
    listeHosts = []
    ipServeurACN = []


    # Création d'un motif pour le scan reseau
    ipSplit = ip.split('.')
    for i in range (0,3):
        ipModele += ipSplit[i] + '.'
    ipModele += '0'

    # debug
    print('=' * 40)
    print('Votre machine possède l\'ip {}.\r\nLe motif de scan sera donc : {}'. format(ip,ipModele))

    # Scan reseau à la recherche de clients
    nm = nmap.PortScanner() # instantiate nmap.PortScanner object
    nm.scan(hosts=ipModele+'/24', arguments='-n -sP')
    for host in nm.all_hosts():
        print('----------------------------------------------------')
        print('Host : %s (%s)' % (host, nm[host].hostname()))
        print('State : %s' % nm[host].state())
        # Creation d'un mappage reseau
        listeHosts.append(host)

    # Sca, port ACN des clients
    print('=' * 40)
    print('Résultats du scan réseau : (True si port Apt-cache-server trouvé.')
    # Pour chacune des machines du réseau, on teste le port d'ACN (par defaut 3142
    for i in listeHosts:
        testPort = portStatus(i, port)
        # Si réponse True, c'est le serveur
        if testPort == True:
            ipServeurACN.append(i)
            message = 'Eventuel Serveur ACN.'
        else:
            message = 'Pas de port ACN ouvert'
        print(i, ' : ', testPort, '. ', message)

    return ipServeurACN

def validerIpServeurACN(listIp):
    """
    Fonction recupérant la liste des machines susceptibles d'être serveur ACN
    Teste de cette liste pour valider ces IP ou les infirmer
    :param listIp: liste contenant les IP des machines écoutant le port ACN
    :return: IP de la machine sélectionnée comme serveur ACN
    """
    if len(listIp) == 0:
        sys.exit('Aucun serveur ACN de trouver. Merci de vérifier son installation.\r\n'
                 'Relancer ce script sur la machine serveur.\r\n'
                 'Et sélectionner "Installation Serveur"\r\n')
    elif len(listIp) == 1:
        print('Serveur ACN possible : ',listIp[0])
        while True:
            try:
                ouiNon = input("Valider ce choix ? (Oui / Non) ")
                if ouiNon.lower() == 'oui':
                    print('IP du serveur : ', listIp[0] )
                    ipServeur = listIp[0]
                    break
                elif ouiNon.lower() == 'non':
                    sys.exc_info('Revoir la configuration du serveur.\r\n Et relancer ce script.')
            except ValueError:
                print("Oops!  Réponse incorrecte... Réessayer... [Oui / Non ]")
        # Valider l'ip unique
    else:
        print('Plusieurs machines pouvant être des serveurs ACN')
        print('Veuillez sélectionner une ip, merci :')
        for i in enumerate(listIp):
            print('Choix ', i[0] + 1, ' : ', i[1])
        # Installation client
        while True:
            try:
                ipServeur = input("Saisir l'IP du Serveur :")
                if ipTest(ipServeur) is True and ipServeur in listIp:
                    break
            except ValueError:
                print("Oops!  Réponse incorrecte... Réessayer...")
    return ipServeur

# ===========================
# Lancement du script
# ==========================
choixInstall = clientServeur()
if choixInstall.lower() == 'serveur':
    portACN = 3142
    ipServeur = ipRecuperation()
    installServeur(ipServeur,portACN)
else:
    # Installation client
    ip = ipRecuperation()
    portACN = 3142

    ipServeur = chercherServeurACN(ip, portACN)
    ipServeur = validerIpServeurACN(ipServeur)
    installClient(ipServeur,portACN)