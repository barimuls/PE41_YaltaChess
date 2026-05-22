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
                return (debut,joueur_actuel,True)
            else:
                return (debut,joueur_actuel,False)
        
        # Passage au joueur suivant : 0 -> 1 -> 2 -> 0
        joueur_actuel = (joueur_actuel + 1) % 3
        compteur_coups += 1
    
        
    return (-1,-1,False)  # Match nul (limite de coups atteinte)
score_elo_IA_evaluee=1500
score_elo_IA_1=1500
score_elo_IA_2=1500
c=32
for k in range (10) :
    x,a,b=simuler_partie_complete()
    if x>=0:
        delta_1=(score_elo_IA_evaluee-score_elo_IA_1)
        delta_2=(score_elo_IA_evaluee-score_elo_IA_2)
        delta_3=(score_elo_IA_1-score_elo_IA_2)
        E_1=1/(1+10**((delta_1)/400))
        F_1=1/(1+10**(-(delta_1)/400))
        E_2=1/(1+10**((delta_2)/400))
        F_2=1/(1+10**(-(delta_2)/400))
        E_3=1/(1+10**(delta_3/400))
        F_3=1/(1+10**(-(delta_3)/400))
        if b :
        

            score_elo_IA_1,score_elo_IA_evaluee=score_elo_IA_1+c*(0-E_1),score_elo_IA_evaluee+c*(1-F_1)
            score_elo_IA_2,score_elo_IA_evaluee=score_elo_IA_2+c*(0-E_2),score_elo_IA_evaluee+c*(1-F_2)
            score_elo_IA_1,score_elo_IA_2=score_elo_IA_1+c*(0.5-F_3),score_elo_IA_2+c*(0.5-E_3)
        else :
                pass #on finit après