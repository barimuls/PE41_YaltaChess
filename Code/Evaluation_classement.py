
from pathlib import Path
from IA import *
from Plateau import *

classements = Path(__file__).parent / "Elos.txt"

def formule_elo(elo_joueur_0,elo_joueur_1, resultat, k=32):
    # k est un facteur de pondération qui détermine à quel point les classements changent après chaque partie
    # resultat est 1 si le joueur 0 gagne, 0.5 en cas de match nul, et 0 si le joueur 1 gagne
    Ea = 1 / (1 + 10 ** ((elo_joueur_1 - elo_joueur_0) / 400)) # probabilité que le joueur 0 gagne
    Eb = 1-Ea # probabilité que le joueur 1 gagne
    
    nouvel_elo_joueur_0 = elo_joueur_0 + k * (resultat - Ea)
    nouvel_elo_joueur_1 = elo_joueur_1 + k * (1 - resultat - Eb)

    return nouvel_elo_joueur_0, nouvel_elo_joueur_1

def variation_elo(elo_joueur_0,elo_joueur_1, resultat, k=32):
    Ea = 1 / (1 + 10 ** ((elo_joueur_1 - elo_joueur_0) / 400)) # probabilité que le joueur 0 gagne
    Eb = 1-Ea # probabilité que le joueur 1 gagne
    
    variation_elo_joueur_0 = k * (resultat - Ea)

    return variation_elo_joueur_0 # on renvoit que joueur 0

def ajouter_joueur_classement(joueur, elo_initial=1000):
    with open(classements, "r") as f:
        lignes = f.readlines()

    for ligne in lignes:
        nom, _ = ligne.strip().split(";")
        if nom == joueur:
            return  # joueur déjà présent

    with open(classements, "a") as f:
        f.write(f"{joueur};{elo_initial}\n")
        
def reset_classement( elos_initial=1000):
    #mettre tous les classements à 1000
    with open(classements, "r") as f:
        lignes = f.readlines() 

    with open(classements, "w") as f:
        for ligne in lignes:
            nom, _ = ligne.strip().split(";")
            f.write(f"{nom};{elos_initial}\n")

def vider_classement():
    with open(classements, "w") as f:
        f.write("") # on vide le fichier

def afficher_classement():
    with open(classements, "r") as f:
        lignes = f.readlines()

    classement = []
    for ligne in lignes:
        nom, elo = ligne.strip().split(";")
        classement.append((nom, float(elo)))

    classement.sort(key=lambda x: x[1], reverse=True)

    print("Classement des joueurs :")
    for nom, elo in classement:
        print(f"{nom} : {elo}")

def mettre_a_jour_classement_2j(joueur0,joueur1,resultat):
    with open(classements, "r") as f:
        lignes = f.readlines()
    
    classement_joueur0 = None
    classement_joueur1 = None
    
    for ligne in lignes:
        nom, elo = ligne.strip().split(";")
        if nom == joueur0:
            classement_joueur0 = float(elo)
        elif nom == joueur1:
            classement_joueur1 = float(elo)
    
    if classement_joueur0 is not None and classement_joueur1 is not None:
        nouvel_elo_joueur_0, nouvel_elo_joueur_1 = formule_elo(classement_joueur0, classement_joueur1, resultat)
        
        # Mettre à jour les classements dans le fichier
        with open(classements, "w") as f:
            for ligne in lignes:
                nom, elo = ligne.strip().split(";")
                if nom == joueur0:
                    f.write(f"{joueur0};{nouvel_elo_joueur_0}\n")
                elif nom == joueur1:
                    f.write(f"{joueur1};{nouvel_elo_joueur_1}\n")
                else:
                    f.write(ligne)
    else:
        print("Erreur : Un des joueurs n'a pas été trouvé dans le classement.")
        
    #print(classement_joueur0, classement_joueur1)
    #print(nouvel_elo_joueur_0, nouvel_elo_joueur_1)
    print(f"difference de points : {nouvel_elo_joueur_0 - classement_joueur0} pour {joueur0}, {nouvel_elo_joueur_1 - classement_joueur1} pour {joueur1}")

def mettre_a_jour_classement_3j(joueur0,joueur1,joueur2,gagnant):
    ajouter_joueur_classement(joueur0)
    ajouter_joueur_classement(joueur1)
    ajouter_joueur_classement(joueur2)# n'ajoute le joueur que s'il n'est pas déjà présent dans le classement
    
    #gagnant vaut -1 en cas d'égalité
    
    variation_joueur0 = 0
    variation_joueur1 = 0
    variation_joueur2 = 0
    
    with open(classements, "r") as f:
        lignes = f.readlines()
        
    classement_joueur0 = None
    classement_joueur1 = None
    classement_joueur2 = None
    
    for ligne in lignes:
        nom, elo = ligne.strip().split(";")
        if nom == joueur0:
            classement_joueur0 = float(elo)
        if nom == joueur1:
            classement_joueur1 = float(elo)
        if nom == joueur2:
            classement_joueur2 = float(elo)
    
    if classement_joueur0 is None or classement_joueur1 is None or classement_joueur2 is None:
        print("Erreur : Un des joueurs n'a pas été trouvé dans le classement c'est bizzard.")
        return
        
        
    variation_joueur0 += variation_elo(classement_joueur0, classement_joueur1, (1 if gagnant == 0 else 0.5 if gagnant == -1 else 0 if gagnant == 1 else 0.5))
    variation_joueur0 += variation_elo(classement_joueur0, classement_joueur2, (1 if gagnant == 0 else 0.5 if gagnant == -1 else 0 if gagnant == 2 else 0.5))
    
    variation_joueur1 += variation_elo(classement_joueur1, classement_joueur0, (1 if gagnant == 1 else 0.5 if gagnant == -1 else 0 if gagnant == 0 else 0.5))
    variation_joueur1 += variation_elo(classement_joueur1, classement_joueur2, (1 if gagnant == 1 else 0.5 if gagnant == -1 else 0 if gagnant == 2 else 0.5))
        
    variation_joueur2 += variation_elo(classement_joueur2, classement_joueur0, (1 if gagnant == 2 else 0.5 if gagnant == -1 else 0 if gagnant == 0 else 0.5))
    variation_joueur2 += variation_elo(classement_joueur2, classement_joueur1, (1 if gagnant == 2 else 0.5 if gagnant == -1 else 0 if gagnant == 1 else 0.5))

    if joueur0 == joueur1 : # les cas où deux joueurs sont les mêmes 
        variation_joueur0 = (variation_joueur0 + variation_joueur1)
        variation_joueur1 = variation_joueur0
    elif joueur0 == joueur2 :
        variation_joueur0 = (variation_joueur0 + variation_joueur2)
        variation_joueur2 = variation_joueur0
    elif joueur1 == joueur2 :
        variation_joueur1 = (variation_joueur1 + variation_joueur2)
        variation_joueur2 = variation_joueur1    
    elif joueur0 == joueur1 == joueur2 :
        variation_joueur0 , variation_joueur1, variation_joueur2 = 0,0,0
    
    nouvel_elo_joueur_0 = classement_joueur0 + variation_joueur0
    nouvel_elo_joueur_1 = classement_joueur1 + variation_joueur1
    nouvel_elo_joueur_2 = classement_joueur2 + variation_joueur2
        
    with open(classements, "w") as f:
        for ligne in lignes:
            nom, elo = ligne.strip().split(";")
            if nom == joueur0:
                f.write(f"{joueur0};{nouvel_elo_joueur_0}\n")
            elif nom == joueur1:
                f.write(f"{joueur1};{nouvel_elo_joueur_1}\n")
            elif nom == joueur2:
                f.write(f"{joueur2};{nouvel_elo_joueur_2}\n")
            else:
                f.write(ligne)



liste_IA_existantes = [(choisir_coup_aleatoire,None),(choisir_coup_heuristique,None),(choisir_coup_heuristique_v1,None),(choisir_coup_minimax,1),(choisir_coup_minimax,2),(choisir_coup_minimax_ou_on_dejoue,1),(choisir_coup_minimax_ou_on_dejoue,2),(choisir_coup_IA_optimisee_ou_on_dejoue,1),(choisir_coup_IA_optimisee_ou_on_dejoue,2),(choisir_coup_IA_optimisee_parallele,1),(choisir_coup_IA_optimisee_parallele,2),(choisir_coup_IA_optimisee_parallele,3),(choisir_coup_paranoid_alpha_beta,1),(choisir_coup_paranoid_alpha_beta,2),(choisir_coup_paranoid_alpha_beta,3)]

def simuler_partie(IA0 = None, IA1 = None, IA2 = None):
    #choix aléatoire de 3 IA
    if IA0 is None:
        IA0 = random.choice(liste_IA_existantes)
    if IA1 is None:
        IA1 = random.choice(liste_IA_existantes)
    if IA2 is None:
        IA2 = random.choice(liste_IA_existantes)
    IAs = [IA0, IA1, IA2]
    print(f"Les IA choisies sont : {IA0[0].__name__}profondeur {IA0[1]}, {IA1[0].__name__}profondeur {IA1[1]}, {IA2[0].__name__}profondeur {IA2[1]}")
    
    #lancement de la partie
    plateau = creer_plateau()
    plateau.remplir_arete()
    plateau.remplir_pieces_initiales()
    
    compteur_coups = 0
    max_coups = 300
    while(compteur_coups < max_coups and not verifier_victoire(plateau)):
        IA_actuelle = IAs[compteur_coups % 3]
        if IA_actuelle[1] is not None:
            (depart, arrivee) = IA_actuelle[0](plateau, compteur_coups % 3, IA_actuelle[1]) # on choisit le coup
        else: # si il n'y a pas de profondeur
            (depart, arrivee) = IA_actuelle[0](plateau, compteur_coups % 3) 
        jouer_le_coup(plateau, compteur_coups % 3, depart, arrivee)
        
        compteur_coups += 1
        
        if compteur_coups % 10 == 0:
            print(f"Nombre de coups joués : {compteur_coups}")
    
    if verifier_victoire(plateau):
        gagnant = (compteur_coups - 1) % 3
        print(f"Le gagnant est le joueur {gagnant} avec l'IA {IAs[gagnant][0].__name__}profondeur {IAs[gagnant][1]}")   
        mettre_a_jour_classement_3j(f"{IAs[0][0].__name__} profondeur {IAs[0][1]}",f"{IAs[1][0].__name__} profondeur {IAs[1][1]}",f"{IAs[2][0].__name__} profondeur {IAs[2][1]}",gagnant)
    else:
        print("Match nul")
        mettre_a_jour_classement_3j(f"{IAs[0][0].__name__} profondeur {IAs[0][1]}",f"{IAs[1][0].__name__} profondeur {IAs[1][1]}",f"{IAs[2][0].__name__} profondeur {IAs[2][1]}",-1)

if __name__ == "__main__":
    for i in range(4):
        simuler_partie()
        afficher_classement()
    
   
    
    '''
    #test mettre à jour:
    reset_classement()
    mettre_a_jour_classement_3j("IA_optimisee", "IA_optimisee", "IA_optimisee_2", 2)  
    afficher_classement()
    '''
    