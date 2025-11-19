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





