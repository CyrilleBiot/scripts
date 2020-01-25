#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Programme de calcul des scores au tarot"""

__author__ = "Cyrille BIOT"
__copyright__ = "Copyleft"
__credits__ = "Cyrille BIOT"
__license__ = "GPL"
__version__ = "0.1.0"
__date__= "2020/01/25"
__maintainer__ = "Cyrille BIOT"
__email__ = "cyrille@cbiot.fr"
__status__ = "Devel"

import os
import re
import sys
import platform
import subprocess
import socket


# Ubuntu ou DEBIAN
if 'Debian' in platform.version():
    # Si DEBIAN, verif si rooot lance le script
    if not os.geteuid() == 0:
        sys.exit("Only root can run this script")


def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]



def ipTest(ip):
    reg = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
    if re.match(reg, ip):
        return True
    else:
        return False

while True:
    try:
        choixInstall = input("Type d'installation (client/serveur) : ")
        if choixInstall in ['client','serveur']:
            print('Installation de type {}'.format(choixInstall))
            break
        else:
            print('Préciser : client OU serveur.')
            print('ATTENTION A LA CASSE. Pas de majuscule.')
    except ValueError:
        print("Oops!  Réponse incorrecte, ce n'est pas un nombre... Réessayer...")


if choixInstall == 'serveur':
    portACN = 3142

    # Installation SERVEUR
    # Tester si le package apt-cacher-ng est installé ou non
    retval = subprocess.call(["which", "apt-cacher-ng"])
    if retval != 0:
        print("Le package apt-cacher-ng n'est pas intallé. Installation...")
        subprocess.run(['apt-get', 'install','apt-cacher-ng'])

    # Affichage Informations
    print("Le serveur de cache est dès lors opérationnel")
    print("Le port d'écoute est : {}".format(portACN))
    print("Page d'aministration")
    print("Notez bien l'ip de votre serveur, elle vous sera indispensable pour la configuration des clients.")
    print("L'IP du serveur est : ")
    print("Indispensable : cette IP doit être FIXE (réglage sur votre BOX ou serveur DHCP).")
    print(getNetworkIp())

else:
    # Installation client

    while True:
        try:
            ipServeur = input("Saisir l'IP du Serveur :")
            if ipTest(ipServeur) is True:
                break

        except ValueError:

            pat = re.compile("^ (?:(?:25[0-5] | 2[0-4][0-9] |[01]?[0-9][0-9]?)\.){3}(?:25[0-5] | 2[0-4][0-9] |[01]?[0-9][0-9]?)$")

            print("Oops!  Réponse incorrecte, ce n'est pas un nombre... Réessayer...")



    print("Installation client.")
'''
# Reste à insérer l'ip et à le coller au bo n endroit    
    msgApt = 'Acquire::http::Proxy "http://192.168.X.X:3142";'
    fichier = open("/home/ragnarok/data.txt", "a")
    fichier.write("B")
    fichier.close()
'''