Juste un espace de stockage pour quelques scripts.

acn-py
----------

ATTENTION : nouveau git pour ce script  : https://github.com/CyrilleBiot/acn-py/tree/master
Utliser uniquement ce git pour le dev futur

Script automatisant l'installation d'un serveur cache pour apt
Install aussi cron-apt et configuration d'installation UNIQUEMENT automatique
des mises à jour de sécurité
Initialement pour Primtux

TODO
- batteries de test
- Interface graphique (gtk)


Changelog
* Jeudi 6 février, 20:57:00  (UTC+0100)
   Suppression installNmapModule au profit install apt

* Mercredi 5 février, 15:57:00  (UTC+0100)
  Mise en place de l'installation pour les clients et le serveur d'un cron-apt automatisant :
   - la récupération des mises à jour
   - l'installation automatique des mises de sécurité
  Réécriture de baseDebian(). Actif dès en mode install client et serveur
  Ecriture des fonctions
   - installPackage(paquet, distribution) pour automatiser l'installation de paquet .deb
   - portSelection(portACN) --> permet de selectionner un port ACN différent du port par défaut
   - installNmapModule(distrib) --> installation du module nmap si module non installé
  Correction de bugs


* Dimanche 3 février, 15:26:00  (UTC+0100)
  Ajout fonction main()
  Return NONE pour les fonctions qui ne retournent rien
* samedi 2 février 2020, 20:44:51 (UTC+0100)
   Récriture de la fonction de scan reseau
* jeudi 30 janvier 2020, 20:44:51 (UTC+0100)
   Scan réseau (socket, python-nmap)
   Fix des fonctions
* dimanche 26 janvier 2020, 20:44:51 (UTC+0100)
   version 0.1.1
   Opérationnelle, testée sous DEBIAN SID
* mercredi 8 janvier 2020, 20:44:51 (UTC+0100)
   version 0.1.0
   Premier jet, non testé



===================================================
tarot-v3.py
-----------

Juste pour des tests.
TODO
- décompte des points 5 joueurs
- ajout des bonus (petit à la fin, main, chelem, misères...)
- encoder via une classe joueur

TODO ++
Refonte avec tkinter

Changelog
* mercredi 8 janvier 2020, 20:44:51 (UTC+0100)
  version 3.1.1
  Amélioration de la fonction de calcul des points

* mercredi 8 janvier 2020, 13:44:51 (UTC+0100)
  version 3.1.0
  Correction Bug décompte des points
  Correction nommage de variables


===============================================
Digest.php
Patch pour le digest
# Si membres ne souhaitant pas être dans le digest
# leur adresse sont stockées dans un fichier txt
# digest-blacklist.txt
# Racine du site, même niveau que digest.php
# Un membre par ligne avec une fausse entrée. Impératif !

ATTENTION LA PREMIERE LIGNE DOIT AVOIR UNE CHAINE DE CARACTERE QUI NE SERA PAS PRISE NE COMPTE
(c'est un bug qui je ne parviens pas (encore) à résoudre...
Style ABCDEFABCDEFABCDEFABCDEFABCDEF
Pas de guillement, pas de quote, juste le nom d'inscription de l'user chaque ligne
