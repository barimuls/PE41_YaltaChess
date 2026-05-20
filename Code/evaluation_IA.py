import copy
from Plateau import creer_plateau
from FonctionJeux import jouer_le_coup, verifier_victoire
import IA
from random import *

def simuler_partie_complete():
    debut=randint(0,2)
    plateau = creer_plateau()
    plateau.remplir_arete()
    plateau.remplir_pieces_initiales()
    max_coups=300
    profondeur_ia=2
    joueur_actuel = debut
    compteur_coups = 0
    
    while compteur_coups < max_coups:
       
        if joueur_actuel==debut :
            coups = IA.choisir_coup_IA_optimisee_ou_on_dejoue(plateau, joueur_actuel, profondeur_ia)
            
            depart, arrivee = coups[0], coups[1]
            jouer_le_coup(plateau, joueur_actuel, depart, arrivee)
        else:
            coups = IA.choisir_coup_aleatoire(plateau, joueur_actuel)
            depart, arrivee = coups[0], coups[1]
            jouer_le_coup(plateau, joueur_actuel, depart, arrivee)
        # Condition de victoire définie dans votre FonctionJeux.py (nbr_roi < 3)
        if verifier_victoire(plateau, joueur_actuel):
            if joueur_actuel==debut:
                return (joueur_actuel,True)
            else:
                return (joueur_actuel,False)
        
        # Passage au joueur suivant : 0 -> 1 -> 2 -> 0
        joueur_actuel = (joueur_actuel + 1) % 3
        compteur_coups += 1
    
        
    return -1  # Match nul (limite de coups atteinte)
score_elo_IA_evaluee=1500
score_elo_IA_1=1500
score_elo_IA_2=1500
for k in range (100) :
    a,b=simuler_partie_complete()
    if b :
        abs(score_elo_IA_evaluee-score_elo_IA_1)
        abs(score_elo_IA_evaluee-score_elo_IA_2)