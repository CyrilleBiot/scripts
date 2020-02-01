#!/usr/bin/env python

import sys

# Verif que le fichier d'entrée est bien passé en paramètre
if len(sys.argv) == 1:
    print('Usage:' + sys.argv[0] + ' +  Le_nom_du_fichier_à_importer')
    print('Mettre le nom du fichier d\'entrée en argument.')
    exit()
else:
    fileOut = sys.argv[1].split('.')
    fileOut = fileOut[0] + 'Out.txt'

print('Le fichier, après traitement se nommera : {}'. format(fileOut))

# Lecture et recuperation des données
file = open(sys.argv[1], "r")
varFile = file.readlines()
file.close()

# Traitement et creation d'une liste
listVar = []
for ligne in varFile:
    ligne = ligne.strip()
    ligne = ligne.split(' : ')
    strVar = '  * [[' + ligne[1] + ' | ' + ligne[0] + ']]'
    listVar.append(strVar)

# Ecriture des données traitées dans un fichier de sortie
fichierDeSortie = open(fileOut, "a")
for elem in listVar:
    fichierDeSortie.write(elem + "\r\n" )
fichierDeSortie.close()
