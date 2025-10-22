
#----------------------Création d'un plateau----------------------

#------création du graphe------

class Arete:
    def __init__(self, orientation, sommet_arrive):
        self.orientation = orientation  # "chiffre", "lettre", "diag_a1", "diag_h1", "cavalier" ...
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

    def voisin_arete_tour_par_lettre(self):
        voisins=[]
        lettre=str(self.nom[0])
        chiffre=int(self.nom[1:])
        if chiffre==1:
            voisins.append(lettre+str(2))
        elif chiffre==8:
            voisins.append(lettre+str(7))
        elif chiffre==12:
            voisins.append(lettre+str(11))
        else:
            if lettre in {'a','b','c','d'}:
                voisins.append(lettre+str(chiffre+1))
                voisins.append(lettre+str(chiffre-1))
            elif lettre in {'e','f','g','h'}:
                if chiffre !=4 and chiffre !=9:
                    voisins.append(lettre+str(chiffre+1))
                    voisins.append(lettre+str(chiffre-1))
                elif chiffre==4:
                    voisins.append(lettre+str(3))
                    voisins.append(lettre+str(9))
                else: #chiffre==9
                    voisins.append(lettre+str(10))
                    voisins.append(lettre+str(4))
            else: #lettre in {'i','j','k','l'}
                if chiffre !=5 and chiffre !=9:
                    voisins.append(lettre+str(chiffre+1))
                    voisins.append(lettre+str(chiffre-1))
                elif chiffre==5:
                    voisins.append(lettre+str(6))
                    voisins.append(lettre+str(9))
                else: #chiffre==9
                    voisins.append(lettre+str(10))
                    voisins.append(lettre+str(5))
        return voisins
    
    def voisin_arete_tour_par_chiffre(self):
        voisins=[]
        lettre=str(self.nom[0])
        chiffre=int(self.nom[1:])
        if lettre=='a':
            voisins.append('b'+str(chiffre))
        elif lettre=='h':
            voisins.append('g'+str(chiffre))
        elif lettre=='l':
            voisins.append('k'+str(chiffre))
        else:
            if chiffre in {1,2,3,4}:
                voisins.append(chr(ord(lettre) + 1)+str(chiffre))
                voisins.append(chr(ord(lettre) - 1)+str(chiffre))
            elif chiffre in {5,6,7,8}:
                if lettre !='d' and lettre != 'i':
                    voisins.append(chr(ord(lettre) + 1)+str(chiffre))
                    voisins.append(chr(ord(lettre) - 1)+str(chiffre))
                elif lettre =='d':
                    voisins.append('i'+str(chiffre))
                    voisins.append('c'+str(chiffre))
                else: #lettre == 'i'
                    voisins.append('d'+str(chiffre))
                    voisins.append('j'+str(chiffre))


            else:# chiffre in {9,10,11,12}
                if lettre !='e' and lettre != 'i':
                    voisins.append(chr(ord(lettre) + 1)+str(chiffre))
                    voisins.append(chr(ord(lettre) - 1)+str(chiffre))
                elif lettre =='e':
                    voisins.append('i'+str(chiffre))
                    voisins.append('f'+str(chiffre))
                else: #lettre == 'i'
                    voisins.append('e'+str(chiffre))
                    voisins.append('j'+str(chiffre))
                
        return voisins

    def voisin_arete_fou_a1(self):
        voisins=[]
        lettre=str(self.nom[0])
        chiffre=int(self.nom[1:])
        if (lettre=='h' and chiffre==1)or(lettre=='a' and chiffre==8)or(lettre=='l' and chiffre==12):
            return voisins
        elif lettre=='a' or chiffre==1:
            voisins.append(chr(ord(lettre)+1)+str(chiffre+1))
        elif lettre=='h' or chiffre==12 :
            if lettre =='i':
                voisins.append('e'+str(11))
            elif chiffre ==9:
                voisins.append('g'+str(4))
            elif lettre =='e':
                voisins.append('i'+str(11))
            else:
                voisins.append(chr(ord(lettre)-1)+str(chiffre-1))
        elif lettre=='l' or chiffre==8:
            if lettre =='i':
                voisins.append('d'+str(7))
            elif chiffre ==5:
                voisins.append('k'+str(9))
            else:
                voisins.append(chr(ord(lettre)-1)+str(chiffre-1))
        else:

            if chiffre ==4 and lettre in {'e','f','g'}:
                voisins.append(chr(ord(lettre)+1)+str(9))
                voisins.append(chr(ord(lettre)-1)+str(3))
            elif chiffre ==4 and lettre == 'd':
                voisins.append('i'+str(5))
                voisins.append('c'+str(3))
                voisins.append('e'+str(9))
            elif chiffre ==9 and lettre in {'e','f','g'}:
                voisins.append(chr(ord(lettre)-1)+str(4))
                voisins.append(chr(ord(lettre)+1)+str(10))
                if lettre =='e':
                    voisins.append('i'+str(5))
            elif lettre == 'e' and chiffre in {9,10,11}:
                voisins.append(chr(ord(lettre)+1)+str(chiffre+1))
                voisins.append('i'+str(chiffre-1))
            elif lettre == 'i' and chiffre in {9,10,11}:
                voisins.append('e'+str(chiffre+1))
                if chiffre ==9:
                    voisins.append('j'+str(5))
                else :
                    voisins.append('j'+str(chiffre-1))
            elif chiffre ==9 and lettre in {'i','j','k'}:
                voisins.append(chr(ord(lettre)+1)+str(5))
                if lettre =='i':
                    voisins.append('e'+str(10))
                else:
                    voisins.append(chr(ord(lettre)-1)+str(10))
            elif chiffre ==5 and lettre in {'i','j','k'}:
                voisins.append(chr(ord(lettre)+1)+str(6))
                if lettre =='i':
                    voisins.append('e'+str(6))
                    voisins.append('d'+str(4))
                else:
                    voisins.append(chr(ord(lettre)-1)+str(9))
            elif lettre == 'i' and chiffre in {5,6,7}:
                voisins.append(chr(ord(lettre)+1)+str(chiffre+1))
                if chiffre ==5:
                    voisins.append('e'+str(9))
                    voisins.append('d'+str(4))
                else:
                    voisins.append('d'+str(chiffre-1))
            elif lettre == 'd'and chiffre in {5,6,7}:
                voisins.append('i'+str(chiffre+1))
                voisins.append('c'+str(chiffre-1))

            
            else:
                voisins.append(chr(ord(lettre)-1)+str(chiffre-1))
                voisins.append(chr(ord(lettre)+1)+str(chiffre+1))
        return voisins
    
    def voisin_arete_fou_h1(self):
        voisins=[]
        lettre=str(self.nom[0])
        chiffre=int(self.nom[1:])
        
        if (lettre=='a' and chiffre==1)or(lettre=='h' and chiffre==12)or(lettre=='l' and chiffre==8):
            return voisins
        elif lettre=='a' or chiffre==8:
            voisins.append(chr(ord(lettre)+1)+str(chiffre-1))
        elif lettre=='h' or chiffre==1 :
            if chiffre ==4:
                voisins.append('g'+str(9))
            else:
                voisins.append(chr(ord(lettre)-1)+str(chiffre+1))
        elif lettre=='l' or chiffre==12:
            if chiffre ==9:
                voisins.append('k'+str(5))
            else:
                voisins.append(chr(ord(lettre)-1)+str(chiffre+1))
        
        elif chiffre ==4 and lettre in {'f','g'}:
            voisins.append(chr(ord(lettre)-1)+str(9))
            voisins.append(chr(ord(lettre)+1)+str(3))
        elif lettre =='e' and chiffre ==4:
            voisins.append('i'+str(9))
            voisins.append('d'+str(5))
            voisins.append('f'+str(3))
        elif chiffre ==9 and lettre in {'f','g'}:
            voisins.append(chr(ord(lettre)+1)+str(4))
            voisins.append(chr(ord(lettre)-1)+str(10))
        elif lettre == 'e' and chiffre ==9:
            voisins.append('f'+str(4))
            voisins.append('i'+str(10))
        elif lettre == 'e' and chiffre in {10,11}:
            voisins.append(chr(ord(lettre)+1)+str(chiffre-1))
            voisins.append('i'+str(chiffre+1))
        elif lettre == 'i' and chiffre in {10,11}:
            voisins.append('e'+str(chiffre-1))
            voisins.append(chr(ord(lettre)+1)+str(chiffre+1))
        elif chiffre ==9 and lettre == 'i':
            voisins.append('e'+str(4))
            voisins.append('d'+str(5))
            voisins.append('j'+str(10))
        elif chiffre ==9 and lettre in {'j','k'}:
            voisins.append(chr(ord(lettre)-1)+str(5))
            voisins.append(chr(ord(lettre)+1)+str(10))
        elif chiffre ==5 and lettre in {'j','k'}:
            voisins.append(chr(ord(lettre)+1)+str(9))
            voisins.append(chr(ord(lettre)-1)+str(6))
        elif lettre == 'i' and chiffre ==5:
            voisins.append('d'+str(6))
            voisins.append('j'+str(9))
        elif lettre == 'i' and chiffre in {6,7}:
            voisins.append('d'+str(chiffre+1))
            voisins.append(chr(ord(lettre)+1)+str(chiffre-1))
        elif lettre == 'd'and chiffre in {6,7}:
            voisins.append('i'+str(chiffre-1))
            voisins.append(chr(ord(lettre)-1)+str(chiffre+1))
        elif chiffre ==5 and lettre ==5:
            voisins.append('d'+str(4))
            voisins.append('i'+str(9))
            voisins.append('c'+str(6))
        else:
            voisins.append(chr(ord(lettre)+1)+str(chiffre-1))
            voisins.append(chr(ord(lettre)-1)+str(chiffre+1))

        return voisins
    def aretes_appartient_case(self,arete):
        return arete in self.aretes



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
        Affiche le plateau et les arêtes de chaque case
        """
        print("=== STRUCTURE DU PLATEAU ===\n")

        # 1️⃣ Affichage du plateau sous forme de grille
        noms = list(self.sommets.keys())
        noms.sort(key=lambda x: (int(x[1:]), x[0]))
        lignes = sorted(set(int(n[1:]) for n in noms))

        for ligne in lignes:
            cases_ligne = [self.sommets[n] for n in noms if int(n[1:]) == ligne]
            ligne_str = "  ".join(f"{c.nom}:{'x' if c.piece is None else c.piece}" for c in cases_ligne)
            print(ligne_str)
        print("\n")

        # 2️⃣ Affichage des arêtes pour chaque case
        print("=== ARÊTES DU GRAPHE ===\n")
        for nom, case in sorted(self.sommets.items(), key=lambda x: (int(x[0][1:]), x[0][0])):
            if case.aretes:
                aretes_str = ", ".join(f"{a.sommet_arrive} ({a.orientation})" for a in case.aretes)
            else:
                aretes_str = "—"
            print(f"{nom:>4} → {aretes_str}")

    
    def arete_appartient_graph(sommet_depart,arete):
        return sommet_depart.aretes_appartient_case(arete)
        

    #--------------------Remplissage des aretes------------------
    def remplir_arete_tour_chiffre(self):
        for case in self.sommets.values():
            l = case.voisin_arete_tour_par_chiffre()
            for sommet_arrive in l:
                self.ajouter_arete(case.nom,sommet_arrive,'chiffre')
                
    def remplir_arete_tour_lettre(self):
        for case in self.sommets.values():
            l = case.voisin_arete_tour_par_lettre()
            for sommet_arrive in l:
                self.ajouter_arete(case.nom,sommet_arrive,'lettre')

    def remplir_arete_fou_a1(self):
        for case in self.sommets.values():
            l = case.voisin_arete_fou_a1()
            for sommet_arrive in l:
                self.ajouter_arete(case.nom,sommet_arrive,'diag_a1')

    def remplir_arete_fou_h1(self):
        for case in self.sommets.values():
            l = case.voisin_arete_fou_h1()
            for sommet_arrive in l:
                self.ajouter_arete(case.nom,sommet_arrive,'diag_h1')

    def remplir_arete(self):
        self.remplir_arete_tour_chiffre()
        self.remplir_arete_tour_lettre()
        self.remplir_arete_fou_a1()
        self.remplir_arete_fou_h1()


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
    plateau.remplir_arete()
    plateau.afficher()
    #print(plateau.sommets['e9'].aretes)
    #print(f"\nNombre total de cases : {len(plateau.sommets)}")


    