
from pathlib import Path
from IA import *
from Plateau import *
import time
import matplotlib.pyplot as plt

elos= Path(__file__).parent / "Elos.txt" # l'ancien qui contient uniquement les elos, ne jamais modifier
classements = Path(__file__).parent / "Classements.txt" 
ligne1 = "nom;profondeur;elo;temps\n"

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

def ajouter_joueur_classement(joueur,profondeur = None, elo_initial=1000, temps_exe = None):
    with open(classements, "r") as f:
        next(f)
        lignes = f.readlines()

    for ligne in lignes:
        nom, profondeur_act, elo, temps = ligne.strip().split(";")
        if nom == joueur and profondeur_act == str(profondeur):
            return  # joueur déjà présent

    with open(classements, "a") as f:
        f.write(f"{joueur};{profondeur};{elo_initial};{temps_exe}\n")
        
def reset_classement( elos_initial=1000):
    #mettre tous les classements à 1000
    with open(classements, "r") as f:
        next(f,None)  # Ignore la première ligne
        lignes = f.readlines() 

    with open(classements, "w") as f:
        f.write("nom;profondeur;elo;temps\n")
        for ligne in lignes:
            nom, _, _, _ = ligne.strip().split(";")
            f.write(f"{nom};{None};{elos_initial};{None}\n")

def vider_classement():
    with open(classements, "w") as f:
        f.write("nom;profondeur;elo;temps\n") # on vide le fichier

def afficher_classement():
    with open(classements, "r") as f:
        next(f)  # Ignore la première ligne
        lignes = f.readlines()

    classement = []
    for ligne in lignes:
        nom, profondeur, elo, _ = ligne.strip().split(";") 
        classement.append((nom, int(profondeur) if profondeur != "None" else None, int(float(elo))))

    classement.sort(key=lambda x: x[2], reverse=True)

    print("Classement des joueurs :")
    for nom, profondeur, elo in classement:
        if profondeur is not None:
            print(f"{nom} (profondeur {profondeur}) : {elo}")
        else:
            print(f"{nom} : {elo}")

def afficher_classement_graphique(): # a mettre a jour plus tard
    with open(classements, "r") as f:
        next(f)  # Ignore la première ligne
        lignes = f.readlines()

    classement = []
    for ligne in lignes:
        nom, profondeur, elo, _ = ligne.strip().split(";")
        classement.append((nom, int(profondeur) if profondeur != "None" else None, int(float(elo))))

    classement.sort(key=lambda x: x[2], reverse=True)

    elements = [(nom, profondeur) for nom, profondeur, _ in classement]
    noms = [f"{nom} (profondeur {profondeur})" if profondeur is not None else nom for nom, profondeur in elements]
    elos = [elo for _, _, elo in classement]

    plt.figure(figsize=(12, 6))  # largeur, hauteur

    plt.barh(noms, elos)

    plt.xlim(min(elos)-100, max(elos) + 50)  # ajuster les limites de l'axe x
    plt.xlabel("Elo")
    plt.title("Classement des joueurs")

    plt.gca().invert_yaxis()

    plt.subplots_adjust(left=0.35)  # espace pour les noms

    plt.show()

def mettre_a_jour_classement_2j(joueur0,joueur1,resultat):
    with open(classements, "r") as f:
        lignes = f.readlines()
    
    classement_joueur0 = None
    classement_joueur1 = None
    
    for ligne in lignes:
        nom, _, elo, _ = ligne.strip().split(";")
        if nom == joueur0:
            classement_joueur0 = float(elo)
        elif nom == joueur1:
            classement_joueur1 = float(elo)
    
    if classement_joueur0 is not None and classement_joueur1 is not None:
        nouvel_elo_joueur_0, nouvel_elo_joueur_1 = formule_elo(classement_joueur0, classement_joueur1, resultat)
        
        # Mettre à jour les classements dans le fichier
        with open(classements, "w") as f:
            for ligne in lignes:
                nom, _, elo, _ = ligne.strip().split(";")
                if nom == joueur0:
                    f.write(f"{joueur0};{None};{nouvel_elo_joueur_0};{None}\n")
                elif nom == joueur1:
                    f.write(f"{joueur1};{None};{nouvel_elo_joueur_1};{None}\n")
                else:
                    f.write(ligne)
    else:
        print("Erreur : Un des joueurs n'a pas été trouvé dans le classement.")
        
    #print(classement_joueur0, classement_joueur1)
    #print(nouvel_elo_joueur_0, nouvel_elo_joueur_1)
    print(f"difference de points : {nouvel_elo_joueur_0 - classement_joueur0} pour {joueur0}, {nouvel_elo_joueur_1 - classement_joueur1} pour {joueur1}")

def mettre_a_jour_classement_3j(joueur0,joueur1,joueur2,gagnant):
    ajouter_joueur_classement(joueur0[0].__name__, profondeur=joueur0[1])
    ajouter_joueur_classement(joueur1[0].__name__, profondeur=joueur1[1])
    ajouter_joueur_classement(joueur2[0].__name__, profondeur=joueur2[1])# n'ajoute le joueur que s'il n'est pas déjà présent dans le classement
    
    #gagnant vaut -1 en cas d'égalité
    
    variation_joueur0 = 0
    variation_joueur1 = 0
    variation_joueur2 = 0
    
    with open(classements, "r") as f:
        next(f)  # Ignore la première ligne
        lignes = f.readlines()
        
    classement_joueur0 = None
    classement_joueur1 = None
    classement_joueur2 = None
    
    for ligne in lignes:
        nom, profondeur, elo, _ = ligne.strip().split(";")
        if nom == joueur0[0].__name__ and profondeur == str(joueur0[1]):
            classement_joueur0 = float(elo)
        elif nom == joueur1[0].__name__ and profondeur == str(joueur1[1]):
            classement_joueur1 = float(elo)
        elif nom == joueur2[0].__name__ and profondeur == str(joueur2[1]):
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
        f.write(ligne1) # on réécrit la première ligne
        for ligne in lignes:
            nom, profondeur, elo, temps = ligne.strip().split(";")
            if nom == joueur0[0].__name__ and profondeur == str(joueur0[1]):
                f.write(f"{joueur0[0].__name__};{profondeur};{nouvel_elo_joueur_0};{temps}\n")
            elif nom == joueur1[0].__name__ and profondeur == str(joueur1[1]):
                f.write(f"{joueur1[0].__name__};{profondeur};{nouvel_elo_joueur_1};{temps}\n")
            elif nom == joueur2[0].__name__ and profondeur == str(joueur2[1]):
                f.write(f"{joueur2[0].__name__};{profondeur};{nouvel_elo_joueur_2};{temps}\n")
            else:
                f.write(ligne)


#simulation IA
liste_IA_existantes = [(choisir_coup_aleatoire,None),(choisir_coup_heuristique,None),(choisir_coup_heuristique_v1,None),(choisir_coup_minimax,2),(choisir_coup_minimax_ou_on_dejoue,1),(choisir_coup_IA_optimisee_ou_on_dejoue,2),(choisir_coup_IA_optimisee_parallele,3),(choisir_coup_paranoid_alpha_beta,3)]
# les pas interessants :
#liste_IA_pas_interessants = [(choisir_coup_minimax_ou_on_dejoue,2)]

def remplir_IA(liste):
    for IA in liste:
        profondeur_max = IA[1] if IA[1] is not None else None
        if profondeur_max is not None:
            for profondeur in range(1, profondeur_max + 1):
                ajouter_joueur_classement(IA[0].__name__ , profondeur=profondeur)
        else:
            ajouter_joueur_classement(IA[0].__name__, profondeur=None)
def recuperer_IA():
    with open(classements, "r") as f:
        next(f)  # Ignore la première ligne
        lignes = f.readlines()

    IAs = []
    for ligne in lignes:
        nom, profondeur, _, _ = ligne.strip().split(";")
        IAs.append((eval(nom), int(profondeur) if profondeur != "None" else None))
    
    return IAs

def simuler_partie(IA0 = None, IA1 = None, IA2 = None):
    #choix aléatoire de 3 IA
    liste_IA = recuperer_IA()
    
    if IA0 is None:
        IA0 = random.choice(liste_IA)
    if IA1 is None:
        IA1 = random.choice(liste_IA)
    if IA2 is None:
        IA2 = random.choice(liste_IA)
    IAs = [IA0, IA1, IA2]
    print(f"Les IA choisies sont : {IA0[0].__name__} (profondeur {IA0[1]}), {IA1[0].__name__} (profondeur {IA1[1]}), {IA2[0].__name__} (profondeur {IA2[1]})")

    
    #lancement de la partie
    plateau = creer_plateau()
    plateau.remplir_arete()
    plateau.remplir_pieces_initiales()
    
    compteur_coups = 0
    max_coups = 200
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
        print(f"Le gagnant est le joueur {gagnant} avec l'IA {IAs[gagnant][0].__name__} (profondeur {IAs[gagnant][1]})")   
        mettre_a_jour_classement_3j((IAs[0][0], IAs[0][1]), (IAs[1][0], IAs[1][1]), (IAs[2][0], IAs[2][1]), gagnant)
    else:
        print("Match nul")
        mettre_a_jour_classement_3j((IAs[0][0], IAs[0][1]), (IAs[1][0], IAs[1][1]), (IAs[2][0], IAs[2][1]), -1)

def recuperer_position_d_une_partie(nmbre_coups = 10):
    # faire une partie entre IA et récupérer la position après n coups
    plateau = creer_plateau()
    plateau.remplir_arete()
    plateau.remplir_pieces_initiales()
    
    liste_IA = recuperer_IA()
    
    
    IA0 = random.choice(liste_IA)
    IA1 = random.choice(liste_IA)
    IA2 = random.choice(liste_IA)
    IAs = [IA0, IA1, IA2]
    
    
    for i in range(nmbre_coups): # on joue nmbre_coups coups
        IA_actuelle = IAs[i % 3]
        if IA_actuelle[1] is not None:
            (depart, arrivee) = IA_actuelle[0](plateau, i % 3, IA_actuelle[1]) # on choisit le coup
        else: # si il n'y a pas de profondeur
            (depart, arrivee) = IA_actuelle[0](plateau, i % 3) 
        jouer_le_coup(plateau, i % 3, depart, arrivee)
    
    return plateau

def test_temps():
    #test de temps pour les différentes IA
    temps_IA = {}
    plateau = creer_plateau()
    plateau.remplir_arete()
    plateau.remplir_pieces_initiales()
    
    IAs = recuperer_IA()
    
    
    for IA in IAs:
        start_time = time.time()
        if IA[1] is not None:
            IA[0](plateau, 0, IA[1]) # on choisit le coup
        else: # si il n'y a pas de profondeur
            IA[0](plateau, 0) 
        end_time = time.time()
        temps_IA[(IA[0].__name__, IA[1])] = end_time - start_time
        
    with open(classements, "r") as f:
        ligne1 = f.readline()  # Lire la première ligne
        lignes = f.readlines()  # Lire le reste
    
    with open(classements, "w") as f:
        
        f.write(ligne1) # on réécrit la première ligne
        for ligne in lignes:
            nom, profondeur, elo, _ = ligne.strip().split(";")
            if (nom, int(profondeur) if profondeur != "None" else None) in temps_IA:
                f.write(f"{nom};{profondeur};{elo};{temps_IA[(nom, int(profondeur) if profondeur != 'None' else None)]}\n")
            else:
                f.write(ligne)
  
def test_temps_postions(positions):
    #test de temps pour les différentes IA à partir de différentes positions
    temps_IA = {}
    
    IAs = recuperer_IA()
    
    for position in positions:
        for IA in IAs:
            start_time = time.time()
            if IA[1] is not None:
                IA[0](position, 0, IA[1]) # on choisit le coup
            else: # si il n'y a pas de profondeur
                IA[0](position, 0) 
            end_time = time.time()
            if (IA[0].__name__, IA[1]) in temps_IA:
                temps_IA[(IA[0].__name__, IA[1])] += end_time - start_time
            else:
                temps_IA[(IA[0].__name__, IA[1])] = end_time - start_time
    moyenne_temps_IA = {k: v / len(positions) for k, v in temps_IA.items()} # on fait la moyenne des temps pour chaque IA
    
    #on met à jour le fichier classements avec les temps
    with open(classements, "r") as f:
        ligne1 = f.readline()  # Lire la première ligne
        lignes = f.readlines()  # Lire le reste
    with open(classements, "w") as f:
        f.write(ligne1) # on réécrit la première ligne
        for ligne in lignes:
            nom, profondeur, elo, _ = ligne.strip().split(";")
            if (nom, int(profondeur) if profondeur != "None" else None) in moyenne_temps_IA:
                f.write(f"{nom};{profondeur};{elo};{moyenne_temps_IA[(nom, int(profondeur) if profondeur != 'None' else None)]}\n")
            else:
                f.write(ligne)
def afficher_temps():
    with open(classements, "r") as f:
        next(f)  # Ignore la première ligne
        lignes = f.readlines()

    temps_IA = {}
    for ligne in lignes:
        nom, profondeur, _, temps = ligne.strip().split(";")
        if temps != "None":
            temps_IA[(nom, int(profondeur) if profondeur != "None" else None)] = float(temps)

    elements = list(temps_IA.keys())
    noms = [f"{nom} (profondeur {profondeur})" for nom, profondeur in elements]
    temps = list(temps_IA.values())

    plt.figure(figsize=(12, 6))  # largeur, hauteur

    plt.barh(noms, temps)

    plt.xlabel("Temps d'exécution (secondes)")
    plt.title("Temps d'exécution des IA")

    plt.gca().invert_yaxis()

    plt.subplots_adjust(left=0.35)  # espace pour les noms

    plt.show()
    
def afficher_elo_en_fonction_du_temps():
    with open(classements, "r") as f:
        next(f)
        lignes = f.readlines()

    elo_temps = {}
    for ligne in lignes:
        nom, profondeur, elo, temps = ligne.strip().split(";")
        if temps != "None":
            prof = int(profondeur) if profondeur != "None" else None
            elo_temps[(nom, prof)] = (float(elo), float(temps))

    # Marqueurs selon la profondeur
    markers = {None: "o", 1: "s", 2: "D", 3: "^"}

    # Couleur unique par nom d'IA
    noms_uniques = list(dict.fromkeys(nom for nom, _ in elo_temps.keys()))
    palette = plt.cm.tab10.colors
    couleurs = {nom: palette[i % len(palette)] for i, nom in enumerate(noms_uniques)}

    plt.figure(figsize=(12, 6))

    for (nom, profondeur), (elo, temps) in elo_temps.items():
        marker = markers.get(profondeur, "o")
        couleur = couleurs[nom]
        plt.scatter(temps, elo, color=couleur, marker=marker, s=100, zorder=3)

    # Légende couleurs (IAs)
    legende_ias = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=couleurs[nom],
                   markersize=10, label=nom)
        for nom in noms_uniques
    ]

    # Légende marqueurs (profondeurs)
    legende_profondeurs = [
        plt.Line2D([0], [0], marker=m, color="gray", markersize=10,
                   label=f"Profondeur {p if p is not None else 'None'}", linestyle="None")
        for p, m in markers.items()
    ]
    
    leg1 = plt.legend(handles=legende_ias, title="IA",
                      loc="lower right", bbox_to_anchor=(1, 0))
    plt.gca().add_artist(leg1)
    plt.legend(handles=legende_profondeurs, title="Profondeur",
               loc="lower right", bbox_to_anchor=(0.67, 0))  

    plt.xlabel("Temps d'exécution (secondes)")
    plt.ylabel("Elo")
    plt.title("Elo en fonction du temps d'exécution des IA")
    plt.tight_layout()
    plt.show()

def importer_elos():
    with open(elos, "r") as f:
        next(f)  # Ignore la première ligne
        lignes = f.readlines()

    elos_IA = {}
    for ligne in lignes:
        nom_profondeur, elo = ligne.strip().split(";")
        nom, profondeur = nom_profondeur.split(" profondeur ")
        profondeur = int(profondeur) if profondeur != "None" else None
        elos_IA[(nom, profondeur)] = float(elo)

    with open(classements, "r") as f:
        ligne1 = f.readline()  # Lire la première ligne
        lignes_classement = f.readlines()  # Lire le reste

    with open(classements, "w") as f:
        f.write(ligne1) # on réécrit la première ligne
        for nom, profondeur, ancien_elo, temps in (ligne.strip().split(";") for ligne in lignes_classement):
            if (nom, int(profondeur) if profondeur != "None" else None) in elos_IA:
                f.write(f"{nom};{profondeur};{elos_IA[(nom, int(profondeur) if profondeur != 'None' else None)]};{temps}\n")
            else:
                f.write(f"{nom};{profondeur};{ancien_elo};{temps}\n") # si l'IA n'est pas dans elos.txt on garde son ancien elo
            

def matchmaking_selon_classement():
    # faire un matchmaking selon le classement, les IA les plus proches s'affrontent
    with open(classements, "r") as f:
        next(f)  # Ignore la première ligne
        lignes = f.readlines()

    classement = []
    for ligne in lignes:
        nom,profondeur,elo,temps = ligne.strip().split(";")
        classement.append(((nom,int(profondeur) if profondeur != "None" else None), float(elo)))

    classement.sort(key=lambda x: x[1])
    
    for i in range(0, len(classement)-2):
        IA0 = classement[i][0]
        IA1 = classement[i+1][0]
        IA2 = classement[i+2][0]
        print(f"Matchmaking : {IA0} vs {IA1} vs {IA2}")

        simuler_partie((eval(IA0[0]), IA0[1]), (eval(IA1[0]), IA1[1]), (eval(IA2[0]), IA2[1]))
        afficher_classement()

def tourne_pnd_temps(t): # en secondes
    # faire tourner un pnd pendant t secondes, en simulant des parties entre IA
    start_time = time.time()
    compteur_parties = 0
    while time.time() - start_time < t:
        simuler_partie()
        compteur_parties += 1
        if compteur_parties % 10 == 0:
            matchmaking_selon_classement()
            afficher_classement()
            
def sauvegarder_classement():
    with open(classements, "r") as f:
        contenu = f.read()
    with open(classements.with_suffix(".backup.txt"), "w") as f:
        f.write(contenu)
            
def recuperer_sauvegarde_classement():
    with open(classements.with_suffix(".backup.txt"), "r") as f:
        contenu = f.read()
    with open(classements, "w") as f:
        f.write(contenu)

if __name__ == "__main__":
    
    temps = 13*3600 # 13 heures en secondes
    tourne_pnd_temps(temps)

    
    '''
    # on mets les nouveaux temps
    k = 5
    positions = []
    for i in range(k):
        positions.append(recuperer_position_d_une_partie(nmbre_coups=10)) 
        print(f"Position {i+1} récupérée")
    test_temps_postions(positions)
    afficher_temps()
    afficher_elo_en_fonction_du_temps()
    '''
    '''
    #test mettre à jour:
    reset_classement()
    mettre_a_jour_classement_3j("IA_optimisee", "IA_optimisee", "IA_optimisee_2", 2)  
    afficher_classement()
    
    for i in range(4):
        simuler_partie()
        afficher_classement()
    afficher_classement_graphique()
    '''
    