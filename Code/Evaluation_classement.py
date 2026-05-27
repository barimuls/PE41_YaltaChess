from pathlib import Path

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
    if classement_joueur0 is not None and classement_joueur1 is not None and classement_joueur2 is not None:
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
    else:
        print("Erreur : Un des joueurs n'a pas été trouvé dans le classement.") 
    
    
    
if __name__ == "__main__":
    # Exemple d'utilisation
    reset_classement()
    
    ajouter_joueur_classement("IA_optimisee")
    ajouter_joueur_classement("IA_aleatoire")
    ajouter_joueur_classement("IA_optimisee_2")

    mettre_a_jour_classement_3j("IA_optimisee", "IA_optimisee", "IA_optimisee_2", -1)  