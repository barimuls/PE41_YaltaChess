
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
        self.piece = piece  # cav, tour, fou, reine, roi, pion
        self.couleur = None  # couleur du joueur possédant la pièce
        self.aretes = []    # liste d'arêtes (vers autres cases)

    def ajouter_arete(self, orientation, sommet_arrive):
        self.aretes.append(Arete(orientation, sommet_arrive))


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
        Affiche le plateau et les pieces présentes sur chaque case dans la couleur correspondante.
        0 : vert
        1 : rouge
        2 : noir
        """
        print("=== PLATEAU ACTUEL ===\n")

        for ligne in range(1, 13):
            ligne_cases = []
            for lettre in 'abcdefghijkl':
                nom_case = f"{lettre}{ligne}"
                if nom_case in self.sommets:
                    case = self.sommets[nom_case]
                    if case.piece is None:
                        print(f"{nom_case}:  . ", end=" ")
                    else:
                        couleur = case.couleur
                        piece = case.piece
                        if couleur == 0:
                            print(f"\033[32m {nom_case}: {piece} \033[0m", end=" ")
                        elif couleur == 1:
                            print(f"\033[31m {nom_case}: {piece} \033[0m", end=" ")
                        elif couleur == 2:
                            print(f"\033[34m {nom_case}: {piece} \033[0m", end=" ")

            print(" ")
        
        
        print("\n")

    def remplir_pieces_initiales(self):
        #les piece blanches
        self.sommets['a1'].piece='tour'
        self.sommets['a1'].couleur=0
        self.sommets['b1'].piece='cavalier'
        self.sommets['b1'].couleur=0
        self.sommets['c1'].piece='fou'
        self.sommets['c1'].couleur=0
        self.sommets['d1'].piece='reine'
        self.sommets['d1'].couleur=0
        self.sommets['e1'].piece='roi'
        self.sommets['e1'].couleur=0
        self.sommets['f1'].piece='fou'
        self.sommets['f1'].couleur=0
        self.sommets['g1'].piece='cavalier'
        self.sommets['g1'].couleur=0
        self.sommets['h1'].piece='tour'
        self.sommets['h1'].couleur=0
        for lettre in 'abcdefgh':
            nom_case = f"{lettre}2"
            self.sommets[nom_case].piece='pion'
            self.sommets[nom_case].couleur=0

        #les pieces rouges
        self.sommets['a8'].piece='tour' 
        self.sommets['a8'].couleur=1
        self.sommets['b8'].piece='cavalier'
        self.sommets['b8'].couleur=1
        self.sommets['c8'].piece='fou'
        self.sommets['c8'].couleur=1
        self.sommets['d8'].piece='roi'
        self.sommets['d8'].couleur=1
        self.sommets['i8'].piece='reine'
        self.sommets['i8'].couleur=1
        self.sommets['j8'].piece='fou'
        self.sommets['j8'].couleur=1
        self.sommets['k8'].piece='cavalier'
        self.sommets['k8'].couleur=1
        self.sommets['l8'].piece='tour'
        self.sommets['l8'].couleur=1
        for lettre in 'abcdijkl':
            nom_case = f"{lettre}7"
            self.sommets[nom_case].piece='pion'
            self.sommets[nom_case].couleur=1

        #les pieces noires
        self.sommets['h12'].piece='tour'
        self.sommets['h12'].couleur=2
        self.sommets['g12'].piece='cavalier'
        self.sommets['g12'].couleur=2
        self.sommets['f12'].piece='fou'
        self.sommets['f12'].couleur=2
        self.sommets['e12'].piece='reine'
        self.sommets['e12'].couleur=2
        self.sommets['i12'].piece='roi'
        self.sommets['i12'].couleur=2
        self.sommets['j12'].piece='fou'
        self.sommets['j12'].couleur=2
        self.sommets['k12'].piece='cavalier'
        self.sommets['k12'].couleur=2
        self.sommets['l12'].piece='tour'
        self.sommets['l12'].couleur=2
        for lettre in 'efghijkl':
            nom_case = f"{lettre}11"
            self.sommets[nom_case].piece='pion'
            self.sommets[nom_case].couleur=2

    def afficher_aretes(self):
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

    #--------------------Coup possible pour chaque pièce------------------
    def coup_possible_tour_chiffre(self,actuel,couleur,list_coup,deja_vu=[],est_initial=False):
        if actuel in deja_vu:
            return;
        deja_vu.append(actuel);

        #verifier que la case actuelle est disponible
        if self.sommets[actuel].piece is None and not est_initial:
            list_coup.append(actuel);
            for coup_potentiel in self.sommets[actuel].voisin_arete_tour_par_chiffre():
                self.coup_possible_tour_chiffre(coup_potentiel,couleur,list_coup,deja_vu)
            return;
        elif self.sommets[actuel].piece is not None and self.sommets[actuel].couleur == couleur:
            return;
        elif self.sommets[actuel].piece is not None and self.sommets[actuel].couleur != couleur:
            list_coup.append(actuel);
            return;
        else: #est_initial == True
            for coup_potentiel in self.sommets[actuel].voisin_arete_tour_par_chiffre():
                self.coup_possible_tour_chiffre(coup_potentiel,couleur,list_coup,deja_vu)
            return;

    def coup_possible_tour_lettre(self,actuel,couleur,list_coup,deja_vu=[],est_initial=False):
        if actuel in deja_vu:
            return;
        deja_vu.append(actuel);

        #verifier que la case actuelle est disponible
        if self.sommets[actuel].piece is None and not est_initial:
            list_coup.append(actuel);
            for coup_potentiel in self.sommets[actuel].voisin_arete_tour_par_lettre():
                self.coup_possible_tour_lettre(coup_potentiel,couleur,list_coup,deja_vu)
            return;
        elif self.sommets[actuel].piece is not None and self.sommets[actuel].couleur == couleur:
            return;
        elif self.sommets[actuel].piece is not None and self.sommets[actuel].couleur != couleur:
            list_coup.append(actuel);
            return;
        else: #est_initial == True
            for coup_potentiel in self.sommets[actuel].voisin_arete_tour_par_lettre():
                self.coup_possible_tour_lettre(coup_potentiel,couleur,list_coup,deja_vu)
            return;

    def coup_possible_tour(self,depart):
        couleur = self.sommets[depart].couleur
        coups = []
        self.coup_possible_tour_chiffre(depart,couleur,coups,est_initial=True);
        self.coup_possible_tour_lettre(depart,couleur, coups,est_initial=True);
        return coups

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

def coup_est_valide(plateau, piece, depart, arrivee):
    #vérifier que la pièce existe à la case de départ
    if depart not in plateau.sommets or arrivee not in plateau.sommets:
        return False
    if plateau.sommets[depart].piece != piece:
        return False
    #différentes règles de déplacement selon la pièce
    if piece == 'tour':
        coups_possibles = plateau.coup_possible_tour(depart)
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

def tour_de_jeu(plateau, joueur):
    #récuperer le coup
    print (f"C'est le tour du joueur {joueur}.");
    piece = input ("Entrez la pièce à jouer : ");
    depart = input ("Entrez la case de départ : ");
    arrivee = input ("Entrez la case d'arrivée : ");
    #vérifier la validité du coup
    if not coup_est_valide(plateau, piece, depart, arrivee):
        print("Coup invalide. Veuillez réessayer.")
        return tour_de_jeu(plateau, joueur)
    #effectuer le coup
    plateau.sommets[depart].piece = None;
    plateau.sommets[arrivee].piece = piece;
    plateau.sommets[arrivee].couleur = joueur;

    #verifier la condition de victoire
    if verifier_victoire(plateau, joueur):
        print(f"Le joueur {joueur} a gagné la partie!")
        return ;
    
    #afficher le plateau
    plateau.afficher();

    #passer au joueur suivant
    tour_de_jeu(plateau, (joueur+1) %3);

#----------------------Test----------------------
if __name__ == "__main__":
    plateau = creer_plateau()
    plateau.remplir_arete()
    plateau.remplir_pieces_initiales()
    plateau.afficher()
    tour_de_jeu(plateau, 0)
    #print(plateau.sommets['e9'].aretes)
    #print(f"\nNombre total de cases : {len(plateau.sommets)}")


    