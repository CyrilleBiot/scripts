# Gestion du nombre de joueurs
from typing import List

nb_joueurs = -1
while True:
    try:
        print('Entre 3 et 5 joueurs, svp.')
        nb_joueurs = int(input("Saisir le nombre de joueurs : "))
        if 2 < nb_joueurs < 6:
            print("Nombre de joueurs : ", nb_joueurs)
            break
    except ValueError:
        print("Oops!  Réponse incorrecte, ce n'est pas un nombre... Réessayer...")
#  ===================================================


# Creation d'un dictionnaire de joueurs
dico_joueurs = dict()

for i in range (0, nb_joueurs):
    joueur = input("Nom du joueur {} : ".format(i+1) )
    print(joueur)

    # Initialisation des scores
    # Tout le monde à zéro
    dico_joueurs[joueur] = [0]

for nom, point in dico_joueurs.items():
    print("Le joueur {} débute avec {} point.".format(nom, point[0]))
# ===================================================



# Creation d'un dictionnaire de contrat
dico_contrat = dict()
dico_contrat['petite'] = 25
dico_contrat['garde'] = 25 * 2
dico_contrat['garde sans '] = 25 * 4
dico_contrat['garde contre'] = 25 * 6


# Gestion des oudlers

# Création d'un dictionnaire d'oudlers
dico_oudlers = dict()
dico_oudlers[0] = 56
dico_oudlers[1] = 51
dico_oudlers[2] = 41
dico_oudlers[3] = 36





# Les fonctions

def verificationContrat(nombre_de_points, nombre_d_oudlers) :
    # Contrat rempli ou non  ? Calcul du bonus / malus
    if nombre_de_points >= nombre_d_oudlers:
        print("Le contrat est rempli.")
    else:
        print("Le contrat n'est pas rempli.")

    gain = nombre_de_points - nombre_d_oudlers

    print("{} points remportés dans ce tour.". format(gain))
    return gain
#  ===================================================

def updateScore(gain, dictionnaire_joueurs, preneur, nb_joueurs):
    # Mise à jour du score
    # Ajout des scores

    for nom in dictionnaire_joueurs:
        score = dictionnaire_joueurs[nom][-1]

        if nom == preneur:
             score = score + (gain + dico_contrat[contrat_tour]) * (nb_joueurs - 1)
        else:
            score = score - (gain + dico_contrat[contrat_tour])
        dictionnaire_joueurs[nom].append(score)

    print(dictionnaire_joueurs)

# Initialisation des paramètres du tour
def parametrageTour(dictionnaire_joueurs,
                    dictionnaire_contrats,
                    dictionnaire_oudlers,
                    nombre_de_points_realises
                    ):

    # Gestion du preneur
    preneur = ""
    while True:
        try:
            preneur = input("Preneur : ")
            if preneur in dico_joueurs:
                print("Le preneur est {}".format(preneur))
                break
            else:
                print("Ce joueur n'existe pas. Réessayer.")
        except ValueError:
            print("Erreur...")
    # ===================================================

    # Gestion du contrat
    contrat_tour = ""
    while True:
        try:
            contrat_tour = input("Contrat : ")
            contrat_tour = contrat_tour.lower()
            if contrat_tour in dico_contrat:
                print("Le contrat est {}".format(contrat_tour))
                break
            else:
                print("Ce contrat n'existe pas. Réessayer.")
        except ValueError:
            print("Erreur...")
    # ===================================================

    # Gestion du nombre d'oudlers
    nb_oudlers = ""
    while True:
        try:
            print('Nombre d\'oudler(s) : 0, 1, 2 ou 3')
            nb_oudlers = int(input("Saisir le nombre d'oudler(s) : "))
            if nb_oudlers in dico_oudlers :
                print("Nombre d'oudler est {}. Il faut réaliser {} points." . format (nb_oudlers, dico_oudlers[nb_oudlers]))
                break
        except ValueError:
            print("Oops!  Réponse incorrecte, ce n'est pas un nombre... Réessayer...")
    # ===================================================

    # Gestion du nombre de points
    while True:
        try:
            nb_points = int(input("Saisir le nombre de points réalisés : "))
            if 0 < nb_points < 92:
                print("Nombre de points réalisés : ", nb_points)
                break
        except ValueError:
            print("Oops!  Réponse incorrecte, ce n'est pas un nombre... Réessayer...")
    #  ===================================================

    return nb_points, nb_oudlers, contrat_tour, preneur



# Lancement du jeu

fin_du_jeu= ''
while fin_du_jeu.lower() != 'quitter':
    parametresTour = parametrageTour(dico_joueurs, dico_contrat, dico_oudlers, nb_joueurs)
    nb_points = parametresTour[0]
    nb_oudlers = parametresTour[1]
    contrat_tour = parametresTour[2]
    preneur = parametresTour[3]
    gain = verificationContrat(nb_points, dico_oudlers[nb_oudlers])
    updateScore(gain, dico_joueurs, preneur, nb_joueurs)
    fin_du_jeu = input('Cesser la partie ? Saisir "Quitter" : ')


else:
    print('on stoppe la partie.')




