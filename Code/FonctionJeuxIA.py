from Plateau import *
import IA
from FonctionJeux import *;

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



#----------------------Test----------------------
if __name__ == "__main__":
    plateau = creer_plateau()
    plateau.remplir_arete()
    
    plateau.remplir_pieces_initiales()
    plateau.afficher()
 
    tour_de_jeu_IA_minimax_ou_on_dejoue(plateau,0)

    #plateau.afficher_aretes()