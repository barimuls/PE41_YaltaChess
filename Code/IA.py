import copy

from Plateau import *;
from FonctionJeux import *;
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
Mate_score=10**9
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
    
        case_roi=fonct_case_roi(plateau,couleur)
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
def fonct_case_roi(plateau,couleur):
    case_roi = None
    for c, s in plateau.sommets.items():
        if s is not None and s.piece == 'roi' and s.couleur == couleur:
            case_roi = c
            break
    return case_roi
def score_v1_pierre(plateau,couleur) :
        roi_pos = fonct_case_roi(plateau, couleur)
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
            return - 4
        s = 0
        s += score_v1(plateau, couleur)           # matériel
        s += score_mobilités(plateau, couleur)    # mobilité
        s += score_pression(plateau, couleur)     # pression sur adversaires
        s += score_securite_roi(plateau, couleur) # sécurité_roi
        return s

#----------------------Fonctions pour l'heuristique----------------------

def calculer_heuristiques(plateau : Plateau) -> list[float]: # liste de taille 3 
    valeur_piece = {'pion':1,'cavalier':3,'fou':4,'tour':5,'dame':8,'roi':1000}
    valeur_piece_attaque_protege = {'pion':1,'cavalier':3,'fou':4,'tour':5,'dame':8,'roi':15}
    
    avantage_materiel = [0,0,0]
    nombre_case_controlees = [0,0,0]
    score_pieces_menacees = [0,0,0]
    score_piece_protegees = [0,0,0]
    for case , _ in plateau.sommets.items():
        if plateau.sommets[case].piece is not None:
            couleur = plateau.sommets[case].couleur
            piece = plateau.sommets[case].piece
            # calcul avantage matériel
            avantage_materiel[couleur] += valeur_piece[piece]
            
            # calcul du controle,menace et protection
            coup_deplacement_mange_protege = plateau.deplacement_mange_protege(case)
            nombre_case_controlees[couleur] += len(coup_deplacement_mange_protege[0]) * 0.01
            score_pieces_menacees[couleur] += sum(valeur_piece_attaque_protege[plateau.sommets[case].piece] for case in coup_deplacement_mange_protege[1]) *0.07
            score_piece_protegees[couleur] += sum(valeur_piece_attaque_protege[plateau.sommets[case].piece] for case in coup_deplacement_mange_protege[2]) *0.04
    
    heuristiques = [0,0,0]
    for i in range(3):
        heuristiques[i] = avantage_materiel[i] + nombre_case_controlees[i] + score_pieces_menacees[i] + score_piece_protegees[i]
    
    return heuristiques
            

def calculer_son_avantage( plateau: Plateau, couleur : int) -> float:
    heuristiques = calculer_heuristiques(plateau)
    return heuristiques[couleur] - 0.5*heuristiques[(couleur+1)%3] - 0.5*heuristiques[(couleur+2)%3]

def evaluation_rec_avantage_ou_on_dejoue(plateau, couleur, profondeur):
    if profondeur == 0:
        heuristique=calculer_heuristiques(plateau)
        return [heuristique[0],heuristique[1],heuristique[2],None,None];
    liste_coups = coup_possible(plateau, couleur)

    if not liste_coups:
        heuristique = calculer_heuristiques(plateau)
        return [heuristique[0], heuristique[1], heuristique[2], None, None]
    
    meilleur_score = -float('inf');
    meilleur_coup = None;

    #Evaluer chaque coup
    for coup in liste_coups:
        depart = coup[0]
        for arrivee in coup[1]:
            
            plateau_copie = copy.deepcopy(plateau)
            jouer_le_coup(plateau_copie, couleur, depart, arrivee)

            #Appel récursif pour la couleur suivante
            evaluation = evaluation_rec_avantage_ou_on_dejoue(plateau_copie, (couleur+1)%3, profondeur-1)
            
            heuristic = evaluation[couleur] - 0.5*evaluation[(couleur+1)%3] - 0.5*evaluation[(couleur+2)%3];
            if heuristic > meilleur_score:
                meilleur_score = heuristic
                meilleur_coup = (evaluation[0],evaluation[1],evaluation[2],depart, arrivee)
            #dejouer_le_coup(plateau, couleur, depart, arrivee)
            
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
    roi_pos = fonct_case_roi(plateau, couleur)
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
        s = score_v1_pierre(plateau,c) # sécurité du roi
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

def cases_adjacentes_roi(plateau, case_roi):
    voisins = set()
    voisins |= set(plateau.sommets[case_roi].voisin_arete_tour_par_chiffre())
    voisins |= set(plateau.sommets[case_roi].voisin_arete_tour_par_lettre())
    voisins |= set(plateau.sommets[case_roi].voisin_arete_fou_a1())
    voisins |= set(plateau.sommets[case_roi].voisin_arete_fou_h1())
    return voisins

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

             jouer_le_coup(plateau_copie, couleur, depart, arrivee)
                     
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
def evaluation_rec_heuristique_v1(plateau, couleur, profondeur):
    if profondeur == 0:
        return [score_v1_pierre(plateau,0),score_v1_pierre(plateau,1),score_v1_pierre(plateau,2),None,None];
    
    #recupérer tous les coups possibles pour la couleur actuelle
    liste_coups = coup_possible(plateau, couleur)

def evaluation_rec_heuristique_ou_on_dejoue(plateau, couleur, profondeur):
    if profondeur == 0:
        return [score_v1_pierre(plateau,0),score_v1_pierre(plateau,1),score_v1_pierre(plateau,2),None,None];
    
    #recupérer tous les coups possibles pour la couleur actuelle
    liste_coups = coup_possible(plateau, couleur)

    meilleur_score = -float('inf');
    meilleur_coup = None;

    #Evaluer chaque coup
    for coup in liste_coups:
        depart = coup[0]
        for arrivee in coup[1]:

            jouer_le_coup(plateau, couleur, depart, arrivee)

            #Appel récursif pour la couleur suivante
            evaluation = evaluation_rec_heuristique_ou_on_dejoue(plateau, (couleur+1)%3, profondeur-1)
            #print(evaluation)
            heuristic = evaluation[couleur] - 0.5*evaluation[(couleur+1)%3] - 0.5*evaluation[(couleur+2)%3];
            
            heuristic = evaluation[couleur%3] - 0.5*evaluation[(couleur+1)%3] - 0.5*evaluation[(couleur+2)%3];
            if heuristic > meilleur_score:
                meilleur_score = heuristic
                meilleur_coup = (evaluation[0],evaluation[1],evaluation[2],depart, arrivee)

            dejouer_le_coup(plateau, couleur, depart, arrivee)
            
    return meilleur_coup;

def evaluation_rec_heuristique_ou_on_dejoue_v1(plateau, couleur, profondeur):
    if profondeur == 0:
        return [score_v1_pierre(plateau,0),score_v1_pierre(plateau,1),score_v1_pierre(plateau,2),None,None];
    
    #recupérer tous les coups possibles pour la couleur actuelle
    liste_coups = coup_possible(plateau, couleur)

def choisir_coup_minimax(plateau , couleur):
    meilleur_coup = evaluation_rec_heuristique(plateau, couleur, 2)
    return (meilleur_coup[3], meilleur_coup[4]);

def choisir_coup_minimax_ou_on_dejoue(plateau , couleur):
    plateau_copie = copy.deepcopy(plateau)
    meilleur_coup = evaluation_rec_heuristique_ou_on_dejoue(plateau_copie, couleur, 1)
    return (meilleur_coup[3], meilleur_coup[4]);
def choisir_coup_IA_optimisee_ou_on_dejoue(plateau , couleur , profondeur=1 ):
    plateau_copie = copy.deepcopy(plateau) #criminel
    meilleur_coup = evaluation_rec_avantage_ou_on_dejoue(plateau_copie, couleur, profondeur)
    return (meilleur_coup[3], meilleur_coup[4]);

def est_attaquee_par(plateau, case, couleur):
    for c in plateau.sommets:
        s = plateau.sommets[c]
        if s.piece is not None and s.couleur == couleur:
            if case in plateau.coup_possible(c):
                return True
    return False
def nombre_attaquants(plateau, case, couleur):
    n = 0
    for c in plateau.sommets:
        s = plateau.sommets[c]
        if s.piece is not None and s.couleur == couleur:
            if case in plateau.coup_possible(c):
                n += 1
    return n


if __name__ == "__main__":
    
    plateau = creer_plateau()
    plateau.remplir_arete()
    
    plateau.remplir_pieces_initiales()
    #print('heuristiques : ',calculer_heuristiques(plateau))
    
    # print(plateau.deplacement_mange_protege("a2"))
    # print(plateau.deplacement_mange_protege("a1"))
    # print(plateau.deplacement_mange_protege("b1"))
    
    # plateau.sommets["a3"].piece = "tour"
    # plateau.sommets["a3"].couleur = 1
    
    # print('heuristiques : ',calculer_heuristiques(plateau))
    
    # print(plateau.deplacement_mange_protege("b1"))
    
    
    import time
    
    #test temps choisir coup
    k =10
    profondeur = 1
    start_time = time.time()    
    for _ in range(k):
        choisir_coup_IA_optimisee_ou_on_dejoue(plateau,profondeur)
    end_time = time.time()
    print(f"Moyenne temps : {k} coup , profondeur {profondeur}: choisir_coup_IA_optimisee_ou_on_dejoue: {(end_time - start_time) / k:.4f} secondes")
    
    profondeur = 3
    start_time = time.time()    
    for _ in range(k):
        choisir_coup_IA_optimisee_ou_on_dejoue(plateau,profondeur)
    end_time = time.time()
    print(f"Moyenne temps : {k} coup , profondeur {profondeur}: choisir_coup_IA_optimisee_ou_on_dejoue: {(end_time - start_time) / k:.4f} secondes")
    
    profondeur = 1
    start_time = time.time()    
    for _ in range(k):
        choisir_coup_IA_optimisee_ou_on_dejoue(plateau,profondeur)
    end_time = time.time()
    print(f"Moyenne temps : {k} coup , profondeur {profondeur}: choisir_coup_IA_optimisee_ou_on_dejoue: {(end_time - start_time) / k:.4f} secondes")
    
    
    
    # ---- teste du temps des heuristiques ----
    # k = 100
    
    # start_time = time.time()    
    # for _ in range(k):
    #     calculer_heuristiques(plateau)
    # end_time = time.time()
    # print(f"Moyenne des temps pour {k} calculs d'heuristiques avec calculer_heuristiques: {(end_time - start_time) / k:.4f} secondes")
    
    # start_time = time.time()    
    # for _ in range(10):
    #     heuristic(plateau,1)
    # end_time = time.time()
    # print(f"Moyenne des temps pour {k} calculs d'heuristiques avec heuristic: {(end_time - start_time) / k:.4f} secondes")
   
    
    # start_time = time.time()    
    # for _ in range(k):
    #     heuristique_v1 (plateau,1)
    # end_time = time.time()
    # print(f"Moyenne des temps pour {k} calculs d'heuristiques avec heuristique_v1: {(end_time - start_time) / k:.4f} secondes")
    
    
    
    
    
    
    
    