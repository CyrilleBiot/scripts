#!/bin/sh
#
# cyrille <cyrille@cbiot.fr>
# Licence GPL
#
# BUT : que le fond d'écran change toutes les heures
# en fonction d'image situées dans un dossier prédéfini
# 24 images. Une par heure
# 00.png pour 00 heure à 23.png pour 24 heures
#
#
# ===================================
# Declaration des variables
# emplacement de stockage des images
  imgStock=/home/serveur/Images
  defExtension=png
# ===================================
#
#
#
# A positionner sur un cron, sur chaque heure
# A lancer au démarrage de la session
# Si hibernation ou veille, à configurer via pm-utils
#

# =================================================================

# Gestion de la variable d'environnement DBUS_SESSION_BUS_ADDRESS
# =================================================================

# Decommenter cette ligne si Mint 18
  export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pidof -s xfce4-session)/environ |cut -d"=" -f2-)

# Decommenter cette ligne si MINT 19
# export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"

# Compteur initialisé
  cmptImg=0


# Ce répertoire doit contenir 24 images numérotées de 00 à 23
  echo "Test de la validité du répertoire"
  nbImgRep=`ls -1 $imgStock | wc -l`
  echo "Il y $nbImgRep  fichiers dans le répertoire. OK"


# Test Nombre exact d'image dans le répertoire
  if [ $nbImgRep = 24 ]; then
     echo "Nombre d'images dans rep stockage : OK"
     else
     echo "Nombre d'images dans rep stockage : NOT OK"
     echo "Le répertoire doit contenir 24 images."
     echo "Vérifier qu'il y ait bien 24 fichiers de type $defExtension"
     exit
  fi


# TEST DE LA PRESENCE DES 24 IMAGES AVEC BON NOMMAGE
  for file in `ls -1 $imgStock`
      do
        # Analyse du nom du fichier. Séparation nom / extension  
        fullfilename=$(basename $file)
        extension=${fullfilename##*.}
        filename=${fullfilename%.*}
 
      # Test : image 00 pour 00, à 23 pour 23 H....
        if [ "$cmptImg" -eq "$filename" ] ; then
           echo "Fichier Nom : OK"
           else
           echo "Problème nom de fichier. L'image doit être au format HH.extension."
           echo "Exemple : 05.png pour l'image de 5 heures"
           exit
        fi
     
      # Test de l'extension.
        if [ $extension = $defExtension ] ; then
              echo "Extension OK : $extension / $defExtension"
        else
              echo "Probleme extension."
              echo "Mettre des images au format $defExtension"
              exit
        fi

      # DEBUG
        echo "fichier : $file ; Son extension : $extension "
        echo $cmptImg
   
      # Image / fichier suivant(e)
        cmptImg=$(($cmptImg + 1))
      done


# On adapte le wallpaper en fonction de l'heure
  /usr/bin/xfconf-query --channel xfce4-desktop --property /backdrop/screen0/monitor0/workspace0/last-image --set $imgStock/`date +%H`.$defExtension

echo " `date` : $USER " 
echo $USER