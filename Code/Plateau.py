
#----------------------Création d'un plateau----------------------

#------création du graphe------

class Arete:
    def __init__(self, orientation, sommet_arrive):
        self.orientation = orientation  # "vertical", "horizontal", "diag1", "diag2", ...
        self.sommet_arrive = sommet_arrive

    def __repr__(self):
        return f"→ {self.sommet_arrive} ({self.orientation})"


class Case:
    def __init__(self, nom, piece=None):
        self.nom = nom
        self.piece = piece  # {'couleur': 0, 'role': 1}, etc.
        self.aretes = []    # liste d'arêtes (vers autres cases)

    def ajouter_arete(self, orientation, sommet_arrive):
        self.aretes.append(Arete(orientation, sommet_arrive))

    def recuperer_arete_oriente(self,orientation):
        sortie = []
        taille = len(self.aretes)
        for i in range (0,taille-1):
            if (self.aretes[i].orientation == orientation) :
                sortie.append(self.aretes[i])
        return sortie

    def __repr__(self):
        if self.piece is None:
            piece_str = "vide"
        else:
            couleurs = {0: "Blanc", 1: "Noir", 2: "Rouge"}
            roles = {0: "Pion", 1: "Tour", 2: "Cavalier", 3: "Fou", 4: "Reine", 5: "Roi"}

            couleur = couleurs.get(self.piece.get("couleur"), "?")
            role = roles.get(self.piece.get("role"), "?")
            piece_str = f"{couleur} {role}"

        return f"{self.nom} : {piece_str}"


class Graph:
    def __init__(self):
        self.sommets = {}

    def ajouter_case(self, nom, piece=None):
        if nom not in self.sommets:
            self.sommets[nom] = Case(nom, piece)

    def ajouter_arete(self, depart, arrivee, orientation):
        if depart in self.sommets and arrivee in self.sommets:
            self.sommets[depart].ajouter_arete(orientation, arrivee)

    def afficher(self):
        """
        Affiche le plateau ligne par ligne (a1 b1 c1 ... puis a2 b2 ... etc.)
        """
        # Extraire colonnes et lignes à partir des noms de cases existants
        noms = list(self.sommets.keys())

        # Trier d'abord par ligne (numéro), puis par colonne (lettre)
        noms.sort(key=lambda x: (int(x[1:]), x[0]))

        # Identifier toutes les lignes présentes
        lignes = sorted(set(int(n[1:]) for n in noms))

        for ligne in lignes:
            # Récupère toutes les cases de cette ligne (dans l'ordre alphabétique)
            cases_ligne = [self.sommets[n] for n in noms if int(n[1:]) == ligne]
            ligne_str = "  ".join(f"{c.nom}:{'x' if c.piece is None else c.piece}" for c in cases_ligne)
            print(ligne_str)
    

#------Initialisation du plateau hexagonal carré (type Yalta)------

def creer_plateau():
    plateau = Graph()

    # Les combinaisons qui existe
    masque = {
        1:  ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'),
        2:  ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'),
        3:  ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'),
        4:  ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'),
        5:  ('a', 'b', 'c', 'd', 'i', 'j', 'k', 'l'),
        6:  ('a', 'b', 'c', 'd', 'i', 'j', 'k', 'l'),
        7:  ('a', 'b', 'c', 'd', 'i', 'j', 'k', 'l'),
        8:  ('a', 'b', 'c', 'd', 'i', 'j', 'k', 'l'),
        9:  ('e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'),
        10: ('e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'),
        11: ('e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'),
        12: ('e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'),
    }

    # Créer les cases existantes
    for ligne, cols in masque.items():
        for col in cols:
            plateau.ajouter_case(f"{col}{ligne}")
    return plateau


#----------------------Test----------------------
if __name__ == "__main__":
    plateau = creer_plateau()
    plateau.afficher()
    #print(f"\nNombre total de cases : {len(plateau.sommets)}")

