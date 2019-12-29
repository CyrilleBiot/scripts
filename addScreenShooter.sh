#!/bin/sh
#
# 
# Script shell permettant de rajouter
# un screenshooter et de le 
# positionner sur le raccourci
# clavier F1
#
# Pour FLUXBOX 
#
# cyrille <cyrille@cbiot.fr> 9.X.16
#

# Recuperation du USER
  USER=$(whoami)

# Test de l'existence du programme de screenshooter 
if which xfce4-screenshooter > /dev/null; then
    echo "screenshooter already install. Fine."
else
    echo "xfce4-screenshooter does not exist. Go for the installation"
    su -c "apt-get install xfce4-screenshooter"
fi

# Test de la presence de fluxbox
if [ -f "/home/$USER/.fluxbox/keys" ]; then
    echo "Fluxbox OK";
else
    echo "Fluxbox not found. This script works only with it. Install it."
    exit
fi

# Ajouter un raccourci clavier
echo "# Ajout hotkey pour xfce4-screenshooter " >> /home/$USER/.fluxbox/keys
echo "None F1 :ExecCommand xfce4-screenshooter & " >> /home/$USER/.fluxbox/keys


# Avertissement
echo "Think to restart your fluxbox session."


