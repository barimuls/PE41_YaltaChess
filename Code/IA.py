import Plateau;
import random;

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
        depart = coup[0];
        for arrivee in coup[1]:
            #faire le coup
            piece_capturee = plateau.sommets[arrivee].piece;
            couleur_capturee = plateau.sommets[arrivee].couleur;
            plateau.sommets[arrivee].piece = plateau.sommets[depart].piece;
            plateau.sommets[arrivee].couleur = plateau.sommets[depart].couleur;
            plateau.sommets[depart].piece = None;
            plateau.sommets[depart].couleur = None;
            #calculer le score
            h = heuristic(plateau,couleur);
            #annuler le coup
            plateau.sommets[depart].piece = plateau.sommets[arrivee].piece;
            plateau.sommets[depart].couleur = plateau.sommets[arrivee].couleur;
            plateau.sommets[arrivee].piece = piece_capturee;
            plateau.sommets[arrivee].couleur = couleur_capturee;
            if h > meilleur_score:
                meilleur_score = h;
                meilleur_coup = (depart,arrivee);
    return meilleur_coup;

def score(plateau, couleur):
    score = 0;
    valeur_piece = {'pion':1,'cavalier':3,'fou':5,'tour':3,'dame':9,'roi':1000};
    for case in plateau.sommets.items():
        if plateau.sommets[case[0]].piece != None:
            if plateau.sommets[case[0]].couleur == couleur:
                score += valeur_piece[plateau.sommets[case[0]].piece];
    return score;

def heuristic(plateau, couleur):
    return score(plateau, couleur) - 0.5*score(plateau, (couleur+1)%3) - 0.5*score(plateau, (couleur+2)%3);


