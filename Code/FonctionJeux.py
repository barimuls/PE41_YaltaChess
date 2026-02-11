from Plateau import *;

#-------Fonction pour jouer--------------

def coup_est_valide(plateau, depart, arrivee,joueur):
    #vérifier que la pièce existe à la case de départ

    if depart not in plateau.sommets or plateau.sommets[depart].piece is None or  plateau.sommets[depart].couleur != joueur:
        return False
    
    
    piece = plateau.sommets[depart].piece;

    #différentes règles de déplacement selon la pièce
    if piece == 'tour':
        coups_possibles = plateau.coup_possible_tour(depart)
        if arrivee not in coups_possibles:
            return False
    elif piece == 'fou':
        coups_possibles = plateau.coup_possible_fou(depart)
        if arrivee not in coups_possibles:
            return False
    elif piece == 'dame':
        coups_possibles = plateau.coup_possible_dame(depart)
        if arrivee not in coups_possibles:
            return False
    elif piece == 'roi':
        coups_possibles = plateau.coup_possible_roi(depart)
        if arrivee not in coups_possibles:
            return False
    elif piece == 'cavalier':
        coups_possibles = plateau.coup_possible_cavalier(depart)
        if arrivee not in coups_possibles:
            return False
    elif piece == 'pion':
        coups_possibles = plateau.coup_possible_pion(depart)
        if arrivee not in coups_possibles:
            return False
    return True

def verifier_victoire(plateau, joueur):
    #verifier que un roi adverse est capturé
    nbr_roi = 0
    for case in plateau.sommets.values():
        if case.piece == 'roi':
            nbr_roi += 1
    return nbr_roi < 3

def remplir_prise_en_passant(plateau,piece, depart, arrivee, joueur):
    #remplir la prise en passant si le coup est un double avancée de pion
    if piece == 'pion':
        lettre_depart = depart[0]
        chiffre_depart = int(depart[1:])
        lettre_arrivee = arrivee[0]
        chiffre_arrivee = int(arrivee[1:])

        if joueur ==0 and chiffre_depart ==2 and chiffre_arrivee ==4:
            plateau.prise_en_passant[joueur] = lettre_arrivee + '3'
            plateau.pile_prise_en_passant.append((plateau.prise_en_passant[joueur])) # on mets l'état acuel de plateau.prise_en_passant dans la pile 
        elif joueur ==1 and chiffre_depart ==7 and chiffre_arrivee ==5:
            plateau.prise_en_passant[joueur] = lettre_arrivee + '6'
            plateau.pile_prise_en_passant.append((plateau.prise_en_passant[joueur]))
        elif joueur ==2 and chiffre_depart ==11 and chiffre_arrivee ==9:
            plateau.prise_en_passant[joueur] = lettre_arrivee + '10'
            plateau.pile_prise_en_passant.append((plateau.prise_en_passant[joueur]))
        else:
            plateau.prise_en_passant[joueur] = None
            plateau.pile_prise_en_passant.append(None)
    else:
        plateau.pile_prise_en_passant.append(None)

def jouer_le_coup(plateau, joueur, depart, arrivee):
    #effectuer le coup
    piece = plateau.sommets[depart].piece;
    plateau.sommets[depart].piece = None;
    plateau.sommets[depart].couleur = None;
    if plateau.sommets[arrivee].piece is not None:
        plateau.pile_pieces_mangees.append((plateau.sommets[arrivee].piece , plateau.sommets[arrivee].couleur)) 
    else:
        plateau.pile_pieces_mangees.append(None)
    plateau.sommets[arrivee].piece = piece;
    plateau.sommets[arrivee].couleur = joueur;

    #cas ou on roque
    if piece == 'roi':
        #roque à gauche
        if arrivee == 'c1' and joueur ==0:
            plateau.sommets['a1'].piece = None;
            plateau.sommets['a1'].couleur = None;
            plateau.sommets['d1'].piece = 'tour';
            plateau.sommets['d1'].couleur = joueur;
        elif arrivee == 'j8' and joueur ==1:
            plateau.sommets['l8'].piece = None;
            plateau.sommets['l8'].couleur = None;
            plateau.sommets['i8'].piece = 'tour';
            plateau.sommets['i8'].couleur = joueur;
        elif arrivee == 'f12' and joueur ==2:
            plateau.sommets['h12'].piece = None;
            plateau.sommets['h12'].couleur = None;
            plateau.sommets['e12'].piece = 'tour';
            plateau.sommets['e12'].couleur = joueur;
        #roque à droite
        if arrivee == 'g1' and joueur ==0:
            plateau.sommets['h1'].piece = None;
            plateau.sommets['h1'].couleur = None;
            plateau.sommets['f1'].piece = 'tour';
            plateau.sommets['f1'].couleur = joueur;
        elif arrivee == 'b8' and joueur ==1:
            plateau.sommets['a8'].piece = None;
            plateau.sommets['a8'].couleur = None;
            plateau.sommets['c8'].piece = 'tour';
            plateau.sommets['c8'].couleur = joueur;
        elif arrivee == 'k12' and joueur ==2:
            plateau.sommets['l12'].piece = None;
            plateau.sommets['l12'].couleur = None;
            plateau.sommets['j12'].piece = 'tour';
            plateau.sommets['j12'].couleur = joueur;
    
    #cas de la prise en passant
    if piece == 'pion':
        if arrivee == plateau.prise_en_passant[(joueur +1)%3] or arrivee == plateau.prise_en_passant[(joueur +2)%3]:
            chiffre_depart = depart[1:];
            lettre_arrivee = arrivee[0];
            plateau.sommets[lettre_arrivee + chiffre_depart].piece = None;
            plateau.sommets[lettre_arrivee + chiffre_depart].couleur = None;
           
    #cas ou on se deroque
    if piece == 'roi' and plateau.peut_roquer[joueur] != [False,False]:
        if (plateau.peut_roquer[joueur][0] == True) and (plateau.peut_roquer[joueur][1] == True):
            plateau.pile_pour_roque.append((joueur,-1));
        elif (plateau.peut_roquer[joueur][0] == True):
            plateau.pile_pour_roque.append((joueur,0));
        elif (plateau.peut_roquer[joueur][1] == True):
            plateau.pile_pour_roque.append((joueur,1));
        plateau.peut_roquer[joueur] = [False,False];
    else:
        plateau.pile_pour_roque.append(None);
    if piece == 'tour' and plateau.peut_roquer[joueur] != [False,False]:
        if joueur ==0:
            if depart == 'a1' and plateau.peut_roquer[joueur][0] == True:
                plateau.pile_pour_roque.append((joueur,0));
                plateau.peut_roquer[joueur][0] = False;
            elif depart == 'h1' and plateau.peut_roquer[joueur][1] == True:
                plateau.peut_roquer[joueur][1] = False;
                plateau.pile_pour_roque.append((joueur,1));
            else:
                plateau.pile_pour_roque.append(None);
        elif joueur ==1:
            if depart == 'l8' and plateau.peut_roquer[joueur][0] == True:
                plateau.pile_pour_roque.append((joueur,0));
                plateau.peut_roquer[joueur][0] = False;
            elif depart == 'a8' and plateau.peut_roquer[joueur][1] == True:
                plateau.pile_pour_roque.append((joueur,1));
                plateau.peut_roquer[joueur][1] = False;
            else:
                plateau.pile_pour_roque.append(None);
        elif joueur ==2:
            if depart == 'h12' and plateau.peut_roquer[joueur][0] == True:
                plateau.pile_pour_roque.append((joueur,0));
                plateau.peut_roquer[joueur][0] = False;
            elif depart == 'l12' and plateau.peut_roquer[joueur][1] == True:
                plateau.pile_pour_roque.append((joueur,1));
                plateau.peut_roquer[joueur][1] = False;
    else:
        plateau.pile_pour_roque.append(None);
        
    #mettre à jour la prise en passant
    remplir_prise_en_passant(plateau,piece, depart, arrivee, joueur);


def dejouer_le_coup(plateau,joueur ,depart, arrivee): # On cherche à annuler le dernier coup qui a été joué, notament pour les explorations des IAs
    # depart et arrivée est le coup qui a été joué et doit etre annulé

    piece = plateau.sommets[arrivee].piece;
    piece_mangee = plateau.pile_pieces_mangees.pop(); # renvoie [piece, couleur]
    if piece_mangee is not None:
        print("on est passé ligne 177, normalement il faut rendre la piece qui a été mangée" + str(piece_mangee), "à la case " + arrivee)
        plateau.sommets[arrivee].piece = piece_mangee[0];
        plateau.sommets[arrivee].couleur = piece_mangee[1];
    else:
        plateau.sommets[arrivee].piece = None;
        plateau.sommets[arrivee].couleur = None;

    plateau.sommets[depart].piece = piece;
    plateau.sommets[depart].couleur = joueur;

    #cas où on s'est deroqué
    deroquer = plateau.pile_pour_roque.pop();
    if deroquer is not None:
        (couleur, orientation) = deroquer;
        if orientation == -1: # -1 les deux ont été deroqués ce coup ci, 0 à gauche uniquement, 1 à droite uniquement
            plateau.peut_roquer[couleur] = [True,True];
        else:
            plateau.peut_roquer[couleur][orientation] = True;
            
    #cas où on peut ou non prendre en passant
    case_ou_on_peut_prendre_en_passant = plateau.pile_prise_en_passant.pop();
    if case_ou_on_peut_prendre_en_passant is not None:
        plateau.prise_en_passant[joueur] = case_ou_on_peut_prendre_en_passant;
    else:
        plateau.prise_en_passant[joueur] = None

    #attention il y a plein de cas particuliers à gérer (promotion)

def promotion(plateau, arrivee, joueur, nouvelle_piece):
    #changer la pièce à la case d'arrivée
    plateau.sommets[arrivee].piece = nouvelle_piece
    plateau.sommets[arrivee].couleur = joueur

def promotion_test(plateau, arrivee, joueur):
    if plateau.sommets[arrivee].piece == 'pion':
        chiffre_arrivee = int(arrivee[1:])
        if chiffre_arrivee == 12 or chiffre_arrivee ==1 or chiffre_arrivee ==8:
            return True
    return False

def lancer_partie(plateau):
    plateau.remplir_pieces_initiales()
    plateau.afficher()
    tour_de_jeu(plateau, 0)

def afficher_plateau_sur_site(plateau):
    plateau_pieces = {}
    plateau_couleurs = {}
    case = list(plateau.sommets.keys())
    Case = [i.upper() for i in case]
    inttohex = ["blanc","rouge","noir"]
    for i in range(len(case)):
        plateau_pieces[Case[i]] = plateau.sommets[case[i]].piece
        if plateau.sommets[case[i]].couleur != None:
            plateau_couleurs[Case[i]] = inttohex[plateau.sommets[case[i]].couleur]
        else:
            plateau_couleurs[Case[i]] = plateau.sommets[case[i]].couleur
    return plateau_pieces, plateau_couleurs


#---------------------Les différents tours de jeu---------------------
def tour_de_jeu(plateau, joueur):
    #récuperer le coup
    print (f"C'est le tour du joueur {joueur}.");
    depart = input ("Entrez la case de départ : ");
    arrivee = input ("Entrez la case d'arrivée : ");
    #vérifier la validité du coup
    if not coup_est_valide(plateau, depart, arrivee, joueur):

        print("Coup invalide. Veuillez réessayer.")
        return tour_de_jeu(plateau, joueur)
    
    jouer_le_coup(plateau, depart, arrivee, joueur);

    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        print(f"Le joueur {joueur} a gagné la partie!")
        return ;
    
    #afficher le plateau
    plateau.afficher();

    #passer au joueur suivant
    tour_de_jeu(plateau, (joueur+1) %3);

def tour_de_jeu_web(plateau, joueur, depart, arrivee):
    #vérifier la validité du coup
    if not coup_est_valide(plateau, depart, arrivee, joueur):
        return False
    #effectuer le coup

    jouer_le_coup(plateau, joueur, depart, arrivee);

    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        return True
    
    return None

def tour_de_jeu_avec_IA(plateau,joueur):
    if joueur ==0:# le vrai joueur
        print (f"C'est le tour du joueur {joueur}.");
        depart = input ("Entrez la case de départ : ");
        arrivee = input ("Entrez la case d'arrivée : ");
        if not coup_est_valide(plateau, depart, arrivee, joueur):
            print("Coup invalide. Veuillez réessayer.")
            return tour_de_jeu_avec_IA(plateau, joueur)
    else: #IA
        print (f"C'est le tour de l'IA joueur {joueur}.");
        coups = IA.choisir_coup_aleatoire(plateau,joueur);
        depart = coups[0];
        arrivee = coups[1];
    
    jouer_le_coup(plateau, joueur, depart, arrivee);

    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        print(f"Le joueur {joueur} a gagné la partie!")
        return ;
    
    #afficher le plateau
    plateau.afficher();

    #passer au joueur suivant
    tour_de_jeu_avec_IA(plateau, (joueur+1) %3);

def tour_de_jeu_IA_heuristique(plateau,joueur):
    if joueur ==0:# le vrai joueur
        print (f"C'est le tour du joueur {joueur}.");
        depart = input ("Entrez la case de départ : ");
        arrivee = input ("Entrez la case d'arrivée : ");
        if not coup_est_valide(plateau, depart, arrivee, joueur):
            print("Coup invalide. Veuillez réessayer.")
            return tour_de_jeu_avec_IA(plateau, joueur)
    else: #IA
        print (f"C'est le tour de l'IA joueur {joueur}.");
        coups = IA.choisir_coup_heuristique(plateau,joueur);
        depart = coups[0];
        arrivee = coups[1];
    
    jouer_le_coup(plateau, joueur, depart, arrivee);

    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        print(f"Le joueur {joueur} a gagné la partie!")
        return ;
    
    #afficher le plateau
    plateau.afficher();

    #passer au joueur suivant
    tour_de_jeu_IA_heuristique(plateau, (joueur+1) %3);

def tour_de_jeu_avec_IA_web(plateau, depart, arrivee):
    joueur = 0 #le vrai joueur
    if not coup_est_valide(plateau, depart, arrivee, joueur):
        return False

    jouer_le_coup(plateau, joueur, depart, arrivee);
    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        return True
    
    #tour de l'IA
    joueur =1 #IA
    coups = IA.choisir_coup_aleatoire(plateau,joueur);
    depart = coups[0];
    arrivee = coups[1];
    jouer_le_coup(plateau, joueur, depart, arrivee);
    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        return True
    
    #tour de l'IA 2
    joueur =2 #IA
    coups = IA.choisir_coup_aleatoire(plateau,joueur);
    depart = coups[0];
    arrivee = coups[1];
    jouer_le_coup(plateau, joueur, depart, arrivee);
    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        return True 
    
    return None

def tour_de_jeu_IA_heuristique_web(plateau, depart, arrivee):
    joueur = 0 #le vrai joueur
    if not coup_est_valide(plateau, depart, arrivee, joueur):
        return False

    jouer_le_coup(plateau, joueur, depart, arrivee);
    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        return True
    
    #tour de l'IA
    joueur =1 #IA
    coups = IA.choisir_coup_heuristique(plateau,joueur);
    depart = coups[0];
    arrivee = coups[1];
    jouer_le_coup(plateau, joueur, depart, arrivee);
    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        return True
    
    #tour de l'IA 2
    joueur =2 #IA
    coups = IA.choisir_coup_heuristique(plateau,joueur);
    depart = coups[0];
    arrivee = coups[1];
    jouer_le_coup(plateau, joueur, depart, arrivee);
    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        return True 
    
    return None

def tour_de_jeu_IA_minimax(plateau,joueur):
    if joueur ==0:# le vrai joueur
        print (f"C'est le tour du joueur {joueur}.");
        depart = input ("Entrez la case de départ : ");
        arrivee = input ("Entrez la case d'arrivée : ");
        if not coup_est_valide(plateau, depart, arrivee, joueur):
            print("Coup invalide. Veuillez réessayer.")
            return tour_de_jeu_avec_IA(plateau, joueur)
    else: #IA
        print (f"C'est le tour de l'IA joueur {joueur}.");
        coups = IA.choisir_coup_minimax(plateau,joueur);
        depart = coups[0];
        arrivee = coups[1];
    
    jouer_le_coup(plateau, joueur, depart, arrivee);

    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        print(f"Le joueur {joueur} a gagné la partie!")
        return ;
    
    #afficher le plateau
    plateau.afficher();

    #passer au joueur suivant
    tour_de_jeu_IA_minimax(plateau, (joueur+1) %3);

def tour_de_jeu_IA_minimax_ou_on_dejoue(plateau,joueur): 
    if joueur ==0:# le vrai joueur
        print (f"C'est le tour du joueur {joueur}.");
        depart = input ("Entrez la case de départ : ");
        arrivee = input ("Entrez la case d'arrivée : ");
        if not coup_est_valide(plateau, depart, arrivee, joueur):
            print("Coup invalide. Veuillez réessayer.")
            return tour_de_jeu_avec_IA(plateau, joueur)
    else: #IA
        print (f"C'est le tour de l'IA joueur {joueur}.");
        coups = IA.choisir_coup_minimax_ou_on_dejoue(plateau,joueur);
        depart = coups[0];
        arrivee = coups[1];
    
    jouer_le_coup(plateau, joueur, depart, arrivee);

    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        print(f"Le joueur {joueur} a gagné la partie!")
        return ;
    
    #afficher le plateau
    plateau.afficher();

    #passer au joueur suivant
    tour_de_jeu_IA_minimax_ou_on_dejoue(plateau, (joueur+1) %3);

def tour_de_jeu_IA_minimax_web(plateau, depart, arrivee):
    joueur = 0 #le vrai joueur
    if not coup_est_valide(plateau, depart, arrivee, joueur):
        return False

    jouer_le_coup(plateau, joueur, depart, arrivee);
    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        return True
    
    #tour de l'IA
    joueur =1 #IA
    coups = IA.choisir_coup_minimax(plateau,joueur);
    depart = coups[0];
    arrivee = coups[1];
    jouer_le_coup(plateau, joueur, depart, arrivee);
    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        return True
    
    #tour de l'IA 2
    joueur =2 #IA
    coups = IA.choisir_coup_minimax(plateau,joueur);
    depart = coups[0];
    arrivee = coups[1];
    jouer_le_coup(plateau, joueur, depart, arrivee);
    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        return True 
    
    return None

def tour_de_jeu_IA_minimax_web_ou_on_dejoue(plateau, depart, arrivee):
    joueur = 0 #le vrai joueur
    if not coup_est_valide(plateau, depart, arrivee, joueur):
        return False

    jouer_le_coup(plateau, joueur, depart, arrivee);
    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        return True
    
    #tour de l'IA
    joueur =1 #IA
    coups = IA.choisir_coup_minimax_ou_on_dejoue(plateau,joueur);
    depart = coups[0];
    arrivee = coups[1];
    jouer_le_coup(plateau, joueur, depart, arrivee);
    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        return True
    
    #tour de l'IA 2
    joueur =2 #IA
    coups = IA.choisir_coup_minimax_ou_on_dejoue(plateau,joueur);
    depart = coups[0];
    arrivee = coups[1];
    jouer_le_coup(plateau, joueur, depart, arrivee);
    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        return True 
    
    return None

#fonctions_pour_IA
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
def cases_adjacentes_roi(plateau, case_roi):
    voisins = set()
    voisins |= set(plateau.sommets[case_roi].voisin_arete_tour_par_chiffre())
    voisins |= set(plateau.sommets[case_roi].voisin_arete_tour_par_lettre())
    voisins |= set(plateau.sommets[case_roi].voisin_arete_fou_a1())
    voisins |= set(plateau.sommets[case_roi].voisin_arete_fou_h1())
    return voisins
#----------------------Test----------------------
if __name__ == "__main__":
    plateau = creer_plateau()
    plateau.remplir_arete()
    
    plateau.remplir_pieces_initiales()
    plateau.afficher()
 

    #plateau.afficher_aretes()
