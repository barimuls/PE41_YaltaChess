classements = "Elos.tkt"

def formule_elo(elo_joueur_0,elo_joueur_1, resultat, k=10):
    # k est un facteur de pondération qui détermine à quel point les classements changent après chaque partie
    # resultat est 1 si le joueur 0 gagne, 0.5 en cas de match nul, et 0 si le joueur 1 gagne
    Ea = 1 / (1 + 10 ** ((elo_joueur_1 - elo_joueur_0) / 400)) # probabilité que le joueur 0 gagne
    Eb = 1-Ea # probabilité que le joueur 1 gagne
    
    nouvel_elo_joueur_0 = elo_joueur_0 + k * (resultat - Ea)
    nouvel_elo_joueur_1 = elo_joueur_1 + k * (1 - resultat - Eb)

    return nouvel_elo_joueur_0, nouvel_elo_joueur_1

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
        
    print(classement_joueur0, classement_joueur1)
    print(nouvel_elo_joueur_0, nouvel_elo_joueur_1)

def ajouter_joueur_classement(joueur, elo_initial=1000):
    with open(classements, "r") as f:
        lignes = f.readlines()

    for ligne in lignes:
        nom, _ = ligne.strip().split(";")
        if nom == joueur:
            return  # joueur déjà présent

    with open(classements, "a") as f:
        f.write(f"{joueur};{elo_initial}\n")
        
if __name__ == "__main__":
    # Exemple d'utilisation
    ajouter_joueur_classement("IA_optimisee")
    ajouter_joueur_classement("IA_aleatoire")
    mettre_a_jour_classement_2j("IA_optimisee", "IA_aleatoire", 1)  # IA_optimisee gagne contre IA_aleatoire
