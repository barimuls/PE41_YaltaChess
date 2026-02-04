import copy

from Plateau import *;
from FonctionJeux import *;
import random;

# je suis passé par ici

def coup_possible(plateau, couleur):
    liste_coups = [];
    for case in plateau.sommets.items():
        if plateau.sommets[case[0]] != None and plateau.sommets[case[0]].couleur == couleur:
            if plateau.coup_possible(case[0]) != []:
                liste_coups += [ [case[0],plateau.coup_possible(case[0])] ];
    return liste_coups;

def choisir_coup_aleatoire(plateau , couleur):
    liste_coups = [];
    for case in plateau.sommets.items():
        if plateau.sommets[case[0]] != None and plateau.sommets[case[0]].couleur == couleur:
            if plateau.coup_possible(case[0]) != []:
                liste_coups += [ [case[0],plateau.coup_possible(case[0])] ];
    n = random.randint(0,len(liste_coups)-1);
    case_depart = liste_coups[n][0];
    m = random.randint(0,len(liste_coups[n][1])-1);
    case_arrivee = liste_coups[n][1][m];
    return (case_depart,case_arrivee);

def choisir_coup_heuristique(plateau , couleur):
    liste_coups = [];
    for case in plateau.sommets.items():
        if plateau.sommets[case[0]] != None and plateau.sommets[case[0]].couleur == couleur:
            if plateau.coup_possible(case[0]) != []:
                liste_coups += [ [case[0],plateau.coup_possible(case[0])] ];
    meilleur_score = -float('inf');
    meilleur_coup = None;
    for coup in liste_coups:
        depart = coup[0]
        for arrivee in coup[1]:
            # Copie profonde du plateau
            plateau_copie = copy.deepcopy(plateau)

            jouer_le_coup(plateau_copie, couleur, depart, arrivee)
                     
            # Calculer le score
            h = heuristic(plateau_copie, couleur)
            
            if h > meilleur_score:
                meilleur_score = h
                meilleur_coup = (depart, arrivee)

    return meilleur_coup;

def score(plateau, couleur):
    score = 0;
    valeur_piece = {'pion':1,'cavalier':3,'fou':5,'tour':3,'dame':9,'roi':1000};
    for case in plateau.sommets.items():
        if plateau.sommets[case[0]].piece != None:
            if plateau.sommets[case[0]].couleur == couleur:
                score += valeur_piece[plateau.sommets[case[0]].piece];
    return score;
def roi_present(plateau,couleur):
    for case in plateau.sommets.items():
        if plateau.sommets[case[0]].couleur ==couleur and plateau.sommets[case[0]].piece =='roi' :
           return True ;
    return False;
        
def score_v1(plateau, couleur):
    nouveau_score=0;
    valeur_piece = {'pion':1,'cavalier':3.1,'fou':3.6,'tour':4.6,'dame':7.8,'roi':1000};
    for case in plateau.sommets.items():
        if plateau.sommets[case[0]].piece != None:
            if plateau.sommets[case[0]].couleur == couleur:
                nouveau_score += valeur_piece[plateau.sommets[case[0]].piece];
    return nouveau_score;
def score_mobilités(plateau,couleur):
    mobilité=0;
    for case in plateau.sommets.items():
        if plateau.sommets[case[0]].piece != None:
            if plateau.sommets[case[0]].couleur == couleur:
                mobilité+=len(plateau.coup_possible(case[0]));
    return 0.05*mobilité;
def score_pression(plateau, couleur):
    pression = 0
    for case in plateau.sommets:
        s = plateau.sommets[case]
        if s != None and s.couleur != couleur and s.piece != None:
            # si je peux capturer cette pièce
            for case2 in plateau.sommets:
                s2 = plateau.sommets[case2]
                if s2 != None and s2.couleur == couleur:
                    if case in plateau.coup_possible(case2):
                        pression += 0.5
                        break
    return pression   
Mate_score=10^9
def danger_attaquants(n):
    if n <= 0:
        return 0
    if n == 1:
        return 2
    if n == 2:
        return 4
    return 5
def score_securite_roi(plateau, couleur):

    # trouver le roi
    
        case_roi=case_roi(plateau,couleur)
        if case_roi is None:
            return -Mate_score  #roi_capturé
        danger_total = 0
        voisins = cases_adjacentes_roi(plateau, case_roi)

        for v in voisins:

            att1 = nombre_attaquants(plateau, v, (couleur+1)%3)
            att2 = nombre_attaquants(plateau, v, (couleur+2)%3)
            def_ami = nombre_attaquants(plateau, v, couleur)

        danger = 0

        # danger individuel
        danger += danger_attaquants(att1)
        danger += danger_attaquants(att2)
        if att1 > 0 and att2 > 0:
            danger += 3

        # défense (limitée)
        danger -= min(def_ami, 2)

        # étouffement par pièces amies
        if plateau.sommets[v].piece is not None and plateau.sommets[v].couleur == couleur:
            danger += 1

        danger_total += danger

        return -danger_total
def case_roi(plateau,couleur):
    case_roi = None
    for c, s in plateau.sommets.items():
        if s is not None and s.piece == 'roi' and s.couleur == couleur:
            case_roi = c
            break
    return case_roi
#----------------------Test----------------------
        
def heuristic(plateau, couleur):
    return score(plateau, couleur) - 0.5*score(plateau, (couleur+1)%3) - 0.5*score(plateau, (couleur+2)%3);
def heuristique_v1(plateau, couleur):
    """
    Évaluation de la position pour le joueur 'couleur' en prenant en compte :
    - Fin de partie (roi éliminé)
    - Mat possible sur un roi ennemi
    - Menaces sur notre roi
    - Matériel, mobilité, pression, sécurité du roi
    - Comparaison relative avec les adversaires (coefficients alpha/beta)
    """

    Mate_score = 10**9  # valeur pour mat

    # ---------------- Vérification fin de partie et menaces ----------------
    roi_pos = case_roi(plateau, couleur)
    if roi_pos is None:
        return -Mate_score  # notre roi est capturé

    # Vérifier si un roi ennemi est capturable par nos pièces
    for case, s in plateau.sommets.items():
        if s is not None and s.couleur == couleur:
            for coup in plateau.coup_possible(case):
                cible = plateau.sommets[coup]
                if cible is not None and cible.piece == 'roi':
                    return Mate_score  # mat possible sur un roi ennemi

    # Vérifier si notre roi est menacé
    danger = 0
    for case, s in plateau.sommets.items():
        if s is not None and s.couleur != couleur:
            if roi_pos in plateau.coup_possible(case):
                danger += 1
    if danger > 0:
        return -Mate_score // 2  # roi menacé

    # ---------------- Calcul des scores pour chaque joueur ----------------
    scores = []
    for c in [0,1,2]:
        s = 0
        s += score_v1(plateau, c)           # matériel
        s += score_mobilités(plateau, c)    # mobilité
        s += score_pression(plateau, c)     # pression sur adversaires
        s += score_securite_roi(plateau, c) # sécurité du roi
        scores.append(s)

    # ---------------- Coefficients alpha et beta ----------------
    alpha = 0.7  # poids sur adversaires
    beta = 1 - alpha
    pas_leader = scores.index(min(scores))
    adversaires = [scores[(couleur+1)%3], scores[(couleur+2)%3]]

    # Score relatif final
    h = scores[couleur] - alpha * max(adversaires) - beta * scores[pas_leader]

    return h

    
def choisir_coup_heuristique_v1(plateau , couleur):
    liste_coups = [];
    for case in plateau.sommets.items():
        if plateau.sommets[case[0]] != None and plateau.sommets[case[0]].couleur == couleur:
            if plateau.coup_possible(case[0]) != []:
                liste_coups += [ [case[0],plateau.coup_possible(case[0])] ];
    meilleur_score = -float('inf');
    meilleur_coup = None;
    for coup in liste_coups:
        depart = coup[0]
        for arrivee in coup[1]:
             #Copie profonde du plateau
             plateau_copie = copy.deepcopy(plateau)

             Plateau.jouer_le_coup(plateau_copie, couleur, depart, arrivee)
                     
             #Calculer le score
             h = heuristique_v1(plateau_copie, couleur)
            
             if h > meilleur_score:
                meilleur_score = h
                meilleur_coup = (depart, arrivee)

    return meilleur_coup;    
def evaluation_rec_heuristique(plateau, couleur, profondeur):
    if profondeur == 0:
        return [score(plateau,0),score(plateau,1),score(plateau,2),None,None];
    
    #recupérer tous les coups possibles pour la couleur actuelle
    liste_coups = coup_possible(plateau, couleur)

    meilleur_score = -float('inf');
    meilleur_coup = None;

    #Evaluer chaque coup
    for coup in liste_coups:
        depart = coup[0]
        for arrivee in coup[1]:
            # Copie profonde du plateau
            plateau_copie = copy.deepcopy(plateau)

            jouer_le_coup(plateau_copie, couleur, depart, arrivee)

            #Appel récursif pour la couleur suivante
            evaluation = evaluation_rec_heuristique(plateau_copie, (couleur+1)%3, profondeur-1)
            
            heuristic = evaluation[couleur] - 0.5*evaluation[(couleur+1)%3] - 0.5*evaluation[(couleur+2)%3];
            if heuristic > meilleur_score:
                meilleur_score = heuristic
                meilleur_coup = (evaluation[0],evaluation[1],evaluation[2],depart, arrivee)
            
    return meilleur_coup;

def evaluation_rec_heuristique_ou_on_dejoue(plateau, couleur, profondeur):
    if profondeur == 0:
        return [score(plateau,0),score(plateau,1),score(plateau,2),None,None];
    
    #recupérer tous les coups possibles pour la couleur actuelle
    liste_coups = coup_possible(plateau, couleur)

    meilleur_score = float('inf');
    meilleur_coup = None;

    #Evaluer chaque coup
    for coup in liste_coups:
        depart = coup[0]
        for arrivee in coup[1]:

            jouer_le_coup(plateau, couleur, depart, arrivee)

            #Appel récursif pour la couleur suivante
            evaluation = evaluation_rec_heuristique_ou_on_dejoue(plateau, (couleur+1)%3, profondeur-1)
            
            heuristic = evaluation[couleur] - 0.5*evaluation[(couleur+1)%3] - 0.5*evaluation[(couleur+2)%3];
            if heuristic < meilleur_score:
                meilleur_score = heuristic
                meilleur_coup = (evaluation[0],evaluation[1],evaluation[2],depart, arrivee)

            dejouer_le_coup(plateau, couleur, depart, arrivee)
            
    return meilleur_coup;


def choisir_coup_minimax(plateau , couleur):
    meilleur_coup = evaluation_rec_heuristique(plateau, couleur, 3)
    return (meilleur_coup[3], meilleur_coup[4]);

def choisir_coup_minimax_ou_on_dejoue(plateau , couleur):
    meilleur_coup = evaluation_rec_heuristique_ou_on_dejoue(plateau, couleur, 3)
    return (meilleur_coup[3], meilleur_coup[4]);
