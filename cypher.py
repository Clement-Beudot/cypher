#!/usr/bin/env python3
# encoding: utf-8
from fonctions import *

header("Non derterminé", "Non derterminé")

pseudo = recuperer_pseudo()
scores = recup_scores()
# Si l'utilisateur n'a pas encore de score, on l'ajoute
if pseudo not in scores.keys():
	scores[pseudo] = 0 


continuer_jeu = 'O'
choix_menu = '0'

# BOUCLE PRINCIPALE

while(choix_menu != 'Q' and continuer_jeu == 'O'):
	choix_menu = '0'
	enregistrer_scores(scores)
	header(pseudo, scores[pseudo])
	afficher_menu()
	choix_menu = input("\n Votre choix : ").upper()
	header(pseudo, scores[pseudo])
	if(choix_menu == "1"):
		scores[pseudo] = scores[pseudo] + lancer_jeu(pseudo, scores[pseudo], "entrainement")	
	if(choix_menu == "2"):
		scores[pseudo] = scores[pseudo] + lancer_jeu(pseudo, scores[pseudo], "challenge")	
	if(choix_menu == "3"):
		afficher_regles()
	if(choix_menu == "4"):
		afficher_scores(scores)
os.system('cls' if os.name == 'nt' else 'clear')