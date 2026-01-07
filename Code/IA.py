import copy

import Plateau;
import random;

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

            Plateau.jouer_le_coup(plateau_copie, couleur, depart, arrivee)
                     
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
           return True 
    return False
            
def gagnant(plateau) :
    rois_vivants=[]
    for c in range(3):
        if roi_present(plateau,c):
            rois_vivants.append(c)
    if len(rois_vivants)==2 :
        c=
        return 
def nouveau_score(plateau, couleur):
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
                mobilité+=length(plateau.coup_possible(case[0]));
    return 0.05*mobilité;
        
def heuristic(plateau, couleur):
    return score(plateau, couleur) - 0.5*score(plateau, (couleur+1)%3) - 0.5*score(plateau, (couleur+2)%3);
def nouvelle_heuristique(plateau, couleur):
    scores = [nouveau_score(plateau,0)+score_mobilité(plateau,0),nouveau_score(plateau,1)+score_mobilité(plateau,1),nouveau_score(plateau,2)+score_mobilité(plateau,2)];
    alpha = 0.6; #coeff au pif un peu
    beta = 0.2;
    leader=scores.index(max(scores));
    h=scores[couleur]-alpha*max(scores[(couleur+1)%3],scores[(couleur+2)%3])-beta*scores[leader];
    return h;
    
def choisir_coup_nouvelle_heuristique(plateau , couleur):
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

            Plateau.jouer_le_coup(plateau_copie, couleur, depart, arrivee)
                     
            # Calculer le score
            h = nouvelle_heuristique(plateau_copie, couleur)
            
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

            Plateau.jouer_le_coup(plateau_copie, couleur, depart, arrivee)

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

            Plateau.jouer_le_coup(plateau, couleur, depart, arrivee)

            #Appel récursif pour la couleur suivante
            evaluation = evaluation_rec_heuristique_ou_on_dejoue(plateau, (couleur+1)%3, profondeur-1)
            
            heuristic = evaluation[couleur] - 0.5*evaluation[(couleur+1)%3] - 0.5*evaluation[(couleur+2)%3];
            if heuristic < meilleur_score:
                meilleur_score = heuristic
                meilleur_coup = (evaluation[0],evaluation[1],evaluation[2],depart, arrivee)

            Plateau.dejouer_le_coup(plateau, couleur, depart, arrivee)
            
    return meilleur_coup;


def choisir_coup_minimax(plateau , couleur):
    meilleur_coup = evaluation_rec_heuristique(plateau, couleur, 3)
    return (meilleur_coup[3], meilleur_coup[4]);

def choisir_coup_minimax_ou_on_dejoue(plateau , couleur):
    meilleur_coup = evaluation_rec_heuristique_ou_on_dejoue(plateau, couleur, 3)
    return (meilleur_coup[3], meilleur_coup[4]);
