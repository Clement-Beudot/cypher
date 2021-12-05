import os
import pickle
from random import randrange
import time
from math import ceil

# VARIABLES

nom_fichier_scores = "scores"


# FONCTIONS D'INTERFACE

def header(pseudo, scores):
	os.system('cls' if os.name == 'nt' else 'clear')
	print(111 * '#')
	print('#', 107 * ' ', '#')
	print('#\033[77m', "Cypher.py Alpha 0.4.0".center(107), '\033[0m#')
	print('#', 107 * ' ', '#')
	print('#\033[37m', ("Pseudo : {0} ".format(pseudo)).center(107), '\033[0m#')
	print('#\033[37m', ("Score : {0} ".format(scores)).center(107), '\033[0m#')
	print('#', 107 * ' ', '#')
	print(111 * '#')


def afficher_regles():
	"""Cette fonction appelée depuis le menu affiche les règles à l'utilisateur"""

	print("\n\n")
	print("Auteur : Bdo\n".center(111))
	print("Ce petit jeu développé en Python est inspiré du mode \"Hacking de SAS\" du jeu dreadcast.net.\n ")
	print("REGLES DU JEU\n".center(111))
	print("Vous devez trouver une clé numérique de 5 chiffres, l'afficheur numérique vous donne des indications")
	print("sur le résultat final : \n")
	print("\tUn underscore (_) indique que le chiffre n'éxiste pas dans la clé")
	print("\tUn zero (0) indique que le chiffre existe, mais n'est pas dans la bonne position")
	print("\tUn un (1) indique que le chiffre entré est le bon et dans la bonne position\n")
	print("MODE ENTRAINEMENT\n".center(111))
	print("Vous disposez de dix tentatives pour trouver la clé, le nombre de points obtenus")
	print("est égal au nombre de tentatives restantes\n")
	print("MODE CHALLENGE\n".center(111))
	print("A chaque manche, vous disposez de 30 secondes pour trouver la clé.")
	print("Si vous dépassez le temps imparti, votre total de points est égal à la somme du temps restant de chaque ")
	print("tour, multiplié par le nombre de clés trouvées.\n")
	print("Exemple : \n")
	print("\tTour N° 1 (gagné) : il vous restait 12 secondes")
	print("\tTour N° 2 (gagné) : il vous restait 6 secondes")
	print("\tTour N° 3 (perdu) : il vous restait 0 seconde\n")
	print("\tVous gagnez (12 + 6) x 2 = 36 points \n")

	input("\nAppuyez sur Entrée (Enter) pour revenir au menu précédent")

def afficher_scores(scores):

	print("TOP 10 DES SCORES\n")
	for cle, valeur in scores.items():
		print(cle, " : ", valeur)
	input("\nAppuyez sur Entrée (Enter) pour revenir au menu précédent")

def afficher_menu():

	print("\n\t 1 : Mode Entrainement")
	print("\n\t 2 : Mode Challenge")
	print("\n\t 3 : Règles et Infos")
	print("\n\t 4 : Tableau des scores (en développement)")
	print("\n\t Q : Quitter le jeu")

def afficher_progression(cypher_masque, restant, mode):
	pourcentage = 0
	if(mode == "entrainement"):
		titre_restant = "Coups restants : "
		coups_restants = 5 * restant
		barre_restant = "\033[40;31m" + (coups_restants) * "#" + "\033[0m" + (55 - coups_restants) * " " + "#"
	elif(mode == "challenge"):
		titre_restant = "Temps restant (s) : "
		temps_restant = (restant * 50) // 30
		barre_restant = "\033[40;31m" + (temps_restant) * "#" + "\033[0m" + (55 - temps_restant) * " " + "#"

	i = 0
	while(i < 5 ):
		if(cypher_masque[i] == '0'):
			pourcentage = pourcentage + 5
		elif(cypher_masque[i] == '1'):
			pourcentage = pourcentage + 10
		i = i + 1
	titre_pourcentage = pourcentage * 2
	titre_pourcentage = "Progression : " + str(titre_pourcentage) + "%"
	titre_restant = titre_restant + str(restant)

	print("#", (titre_pourcentage).center(51), "#", (titre_restant).center(53), "#")
	print(111 * '#')
	

	print("#\033[40;32m",(pourcentage) * "#","\033[0m",(49 - pourcentage) * " ", "#" + barre_restant)
	print(111 * '#')


def afficher_masque(cypher_masque):

	print("\n\n")
	chiffre = {('0',0):"  ###  ", ('0',1):"  # #  ", ('0',2):"  ###  ", ('1',0):"   #   ", ('1',1):"   #   ", ('1',2):"   #   ", ('#',0):"       ", ('#',1):"       ", ('#',2):"  ###  "}
	i = 0
	while(i < 3):
		affichage_ligne = ""
		j = 0
		while(j < 5):
			affichage_ligne = affichage_ligne + chiffre[cypher_masque[j],i]
			j = j +1
		i = i + 1
		print(affichage_ligne.center(111))
	print("\n\n\n\n")


def afficher_resultats(cypher_a_trouver, points, gagne, cumul):

	if(cumul["total"] == -666):
		print("___________________________________".center(111))
		if(gagne):
			print("Cypher débloqué".center(111))
			print("\n")
			print("La clé était : {0}".format(cypher_a_trouver).center(111))
			print("\n")
			print("Vous gagnez : {0} point(s)".format(points).center(111))
		else:
			print("Cypher vérrouillé".center(111))
			print("\n")
			print("Clé non débloquée".center(111))
			print("\n")
			print("Vous gagnez : {0} point(s)".format(points).center(111))

		print("___________________________________".center(111))
	else:
		print("_____________________________________".center(111))
		if(gagne):
			print("Cypher débloqué".center(111))
			print("\n")
			print("La clé était : {0}".format(cypher_a_trouver).center(111))
			print("\n")
			print("Vous gagnez : {0} point(s) sur ce tour".format(points).center(111))
			print("\n")
			print("Nombre clés trouvées : {0}".format(cumul["nombre_tours"]).center(111))
			print("Temps restant cumulés : {0}".format(cumul["temps_cumule"]).center(111))
			print("\n")
			print("Gains total : {0} points".format(cumul["total"]).center(111))
		else:
			print("Cypher vérrouillé".center(111))
			print("\n")
			print("Clé non débloquée".center(111))
			print("\n")
			print("Vous gagnez : {0} point(s) sur ce tour".format(points).center(111))
			print("\n")
			print("Nombre clés trouvées : {0}".format(cumul["nombre_tours"]).center(111))
			print("Temps restant cumulés : {0}".format(cumul["temps_cumule"]).center(111))
			print("\n")
			print("Gains total : {0} points".format(cumul["total"]).center(111))

		print("_____________________________________".center(111))



# FONCTIONS D'INTERACTIONS AVEC L'UTILISATEUR :

def recuperer_pseudo():
	"""Demande le pseudo pour vérifier s'il éxiste déjà dans les scores."""
	pseudo = '' 
	boucler = True
	while(boucler):
		pseudo = input("\nVeuillez entrer votre pseudo (3 caractères minimum) : ")
		if(not pseudo.isalnum()):
			print("Merci de ne pas ajouter de caractères spéciaux :")
		elif(len(pseudo) < 3):
			print("Merci de choisir un pseudo d'au minimum 3 caractères :")
		else : 
			boucler = False
	return pseudo 

def demander_cle(pseudo):
	cle = ' '
	renvoyer_cle = False
	while(not renvoyer_cle):
		cle = input("\n{0}@cypherus : ".format(pseudo))
		if(len(cle) == 5 and cle.isalnum()):
			renvoyer_cle = True
	return cle



# FONCTIONS DE GESTION DES SCORES :

def recup_scores():
	"""Cette fonction récupère les scores enregistrés si le fichier existe."""
	if os.path.exists(nom_fichier_scores): 
		fichier_scores = open(nom_fichier_scores, "rb")
		scores_depickler = pickle.Unpickler(fichier_scores)
		scores = scores_depickler.load()
		fichier_scores.close()
	else: 
		scores = {}
	return scores

def enregistrer_scores(scores):
	"""Cette fonction se charge d'enregistrer les scores dans le fichier"""
	fichier_scores = open(nom_fichier_scores, "wb")
	scores_pickler = pickle.Pickler(fichier_scores)
	scores_pickler.dump(scores)
	fichier_scores.close()

# FONCTIONS DU JEU

def generer_cypher():
	i = 0
	cypher = "#####"
	while(i < 5):
		chiffre = randrange(10)
		chiffre = str(chiffre)
		temp_cypher = cypher[:i] + chiffre + cypher[i+1:]
		cypher = temp_cypher
		i = i + 1
	return cypher

def masquer_cypher(cypher_masque, cypher_a_trouver, derniere_saisie):
	if(cypher_masque == ' '):
		cypher_masque = 5 * '#'
	else:
		i = 0		
		while(i < 5):
			position = 0
			if(derniere_saisie[i] == cypher_a_trouver[i]):
				temp_cypher_masque = cypher_masque[:i] + "1" + cypher_masque[i+1:]
				cypher_masque = temp_cypher_masque
			else :
				while(position < 5):
					if(derniere_saisie[i] == cypher_a_trouver[position]):
						temp_cypher_masque = cypher_masque[:i] + "0" + cypher_masque[i+1:]
						cypher_masque = temp_cypher_masque
					else:
						temp_cypher_masque = cypher_masque[:i] + "#" + cypher_masque[i+1:]
						cypher_masque = temp_cypher_masque
					position = position + 1
			i = i +1
	return cypher_masque

def lancer_jeu(pseudo, scores, mode):
	
	if(mode == "challenge"):

		points_gagne = {"temps_cumule":0, "nombre_tours":0, "total":0}
		challenge_termine = False

		while(challenge_termine == False):

			cypher_a_trouver = generer_cypher()

			gagne = False
			cypher_masque = ' '
			derniere_saisie = ' '
			cypher_masque = masquer_cypher(cypher_masque, cypher_a_trouver, derniere_saisie)
			header(pseudo, scores)
			
			timestamp_fin  = time.time() + 30
			temps_restant = 30
				
			afficher_progression(cypher_masque, temps_restant, mode)
			afficher_masque(cypher_masque)
			while(temps_restant > 0 and gagne == False):

				derniere_saisie = demander_cle(pseudo)
				cypher_masque = masquer_cypher(cypher_masque, cypher_a_trouver, derniere_saisie)
				temps_restant = ceil(timestamp_fin - time.time())

				header(pseudo, scores)
				afficher_progression(cypher_masque, temps_restant, mode)
				afficher_masque(cypher_masque)

				if(cypher_masque == "11111"):
					if(temps_restant <= 0):
						temps_restant = 0
					points_gagne["temps_cumule"] = points_gagne["temps_cumule"] + temps_restant
					points_gagne["nombre_tours"] = points_gagne["nombre_tours"] + 1
					points_gagne["total"] = points_gagne["temps_cumule"] * points_gagne["nombre_tours"]
					gagne = True
					afficher_resultats(cypher_a_trouver, temps_restant, gagne, points_gagne)
					input("\n\n\nAppuyez sur entrée pour generer une nouvelle clé")
				elif(temps_restant <= 0):
					temps_restant = 0
					afficher_resultats(cypher_a_trouver, temps_restant, gagne, points_gagne)
					challenge_termine = True
					input("\n\n\nAppuyez sur entrée pour retourner au menu")
		return points_gagne["total"]
	
	

	if(mode == "entrainement"):

		points_gagne = {"temps_cumule":0, "nombre_tours":0, "total":-666}
		cypher_a_trouver = generer_cypher()

		gagne = False
		cypher_masque = ' '
		derniere_saisie = ' '
		cypher_masque = masquer_cypher(cypher_masque, cypher_a_trouver, derniere_saisie)
		header(pseudo, scores)

		coups_restants = 10
		afficher_progression(cypher_masque, coups_restants, mode)
		afficher_masque(cypher_masque)
		while(coups_restants > 0 and gagne == False):

			derniere_saisie = demander_cle(pseudo)
			cypher_masque = masquer_cypher(cypher_masque, cypher_a_trouver, derniere_saisie)
			coups_restants = coups_restants - 1

			header(pseudo, scores)
			afficher_progression(cypher_masque, coups_restants, mode)
			afficher_masque(cypher_masque)

			if(cypher_masque == "11111"):
				if(coups_restants == 0):
					coups_restants = 1

				gagne = True
				afficher_resultats(cypher_a_trouver, coups_restants, gagne, points_gagne)
				input("\n\n\nAppuyez sur entrée pour retourner au menu")
			elif(coups_restants == 0):
				afficher_resultats(cypher_a_trouver, coups_restants, gagne, points_gagne)
				input("\n\n\nAppuyez sur entrée pour retourner au menu")
		return coups_restants