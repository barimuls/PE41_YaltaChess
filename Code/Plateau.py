
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
        self.piece = piece  # cav, tour, fou, dame, roi, pion
        self.couleur = None  # couleur du joueur possédant la pièce
        self.aretes = []    # liste d'arêtes (vers autres cases)

    def ajouter_arete(self, orientation, sommet_arrive):
        self.aretes.append(Arete(orientation, sommet_arrive))

    #--------------------Voisins pour les cases------------------
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
        elif lettre =='h':
            if chiffre == 9:
                voisins.append('g'+str(4))
            else:
                voisins.append(chr(ord(lettre)-1)+str(chiffre-1))
        elif chiffre==12:
            if lettre =='e':
                voisins.append('i'+str(11))
            elif lettre in {'f','g','h'}:
                voisins.append(chr(ord(lettre)-1)+str(11))
            else: #i,j,k
                voisins.append(chr(ord(lettre)+1)+str(11))
        elif lettre=='l' or chiffre==8:
            if lettre =='i':
                voisins.append('d'+str(7))
            elif chiffre ==5:
                voisins.append('k'+str(9))
            elif chiffre in {9,10,11}:
                voisins.append('k'+str(chiffre+1))
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
            elif lettre == 'e' and chiffre in {10,11}:
                voisins.append(chr(ord(lettre)+1)+str(chiffre+1))
                voisins.append('i'+str(chiffre-1))
            elif lettre == 'i' and chiffre in {9,10,11}:
                voisins.append('e'+str(chiffre+1))
                if chiffre ==9:
                    voisins.append('j'+str(5))
                else :
                    voisins.append('j'+str(chiffre-1))
            elif chiffre ==9 and lettre in {'j','k'}:
                voisins.append(chr(ord(lettre)+1)+str(5))
                voisins.append(chr(ord(lettre)-1)+str(10))
            elif chiffre ==5 and lettre in {'i','j','k'}:
                voisins.append(chr(ord(lettre)+1)+str(6))
                if lettre =='i':
                    voisins.append('e'+str(9))
                    voisins.append('d'+str(4))
                else:
                    voisins.append(chr(ord(lettre)-1)+str(9))
            elif lettre == 'i' and chiffre in {6,7}:
                voisins.append(chr(ord(lettre)+1)+str(chiffre+1))
                voisins.append('d'+str(chiffre-1))
            elif lettre == 'd'and chiffre in {5,6,7}:
                voisins.append('i'+str(chiffre+1))
                voisins.append('c'+str(chiffre-1))

            
            else:
                if lettre in {'j','k'} and chiffre in {10,11}:
                    voisins.append(chr(ord(lettre)+1)+str(chiffre-1))
                    voisins.append(chr(ord(lettre)-1)+str(chiffre+1))
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
            if lettre=='d' and chiffre==8:
                voisins.append('i'+str(7))
            else:
                voisins.append(chr(ord(lettre)+1)+str(chiffre-1))
        elif lettre=='h' or chiffre==1 :
            if chiffre ==4:
                voisins.append('g'+str(9))
            else:
                voisins.append(chr(ord(lettre)-1)+str(chiffre+1))

        elif lettre=='l':
            if chiffre==9:
                voisins.append('k'+str(5))
            elif chiffre in {10,11,12}:
                voisins.append('k'+str(chiffre-1))
            else:# 5,6,7
                voisins.append('k'+str(chiffre+1))
        elif chiffre ==12:
            if lettre =='i':
                voisins.append('e'+str(11))
            elif lettre in {'j','k'}:
                voisins.append(chr(ord(lettre)-1)+str(11))
            else:# e,f,g 
                voisins.append(chr(ord(lettre)+1)+str(11))
        
        
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
        elif chiffre ==5 and lettre == 'd':
            voisins.append('e'+str(4))
            voisins.append('i'+str(9))
            voisins.append('c'+str(6))
        #cas interieur
        else:
            if lettre in {'j','k'} and chiffre in {10,11}:
                voisins.append(chr(ord(lettre)+1)+str(chiffre+1))
                voisins.append(chr(ord(lettre)-1)+str(chiffre-1))
            else:
                voisins.append(chr(ord(lettre)+1)+str(chiffre-1))
                voisins.append(chr(ord(lettre)-1)+str(chiffre+1))

        return voisins


class Graph:
    def __init__(self):
        self.sommets = {}
        self.prise_en_passant = [None,None,None]  # Pour chaque couleur, la case où un pion peut être pris en passant on mets la case où on peut manger
        self.pile_prise_en_passant= []  # Pile pour annuler les prises en passant, contient pour chaque tour, None ou (couleur, case)
        self.peut_roquer = [[True,True],[True,True],[True,True]] # Pour chaque couleur, si le roi peut encore roquer à gauche et droite
        self.pile_pour_roque = []  # Pile pour annuler les roques, contient pour chaque tour, None ou (couleur, direction)
        self.pile_pieces_mangees = []  # Pile des pièces mangées (pour annuler les coups) contient pour chaque tour, None ou (piece, couleur)

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
        self.sommets['d1'].piece='dame'
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
        self.sommets['i8'].piece='dame'
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
        self.sommets['e12'].piece='dame'
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
    
    def remplir_tutoriel_tour(self):
        self.sommets['a1'].piece='tour'
        self.sommets['a1'].couleur=0

    def afficher_aretes(self):
        print("=== ARÊTES DU GRAPHE ===\n")
        for nom, case in sorted(self.sommets.items(), key=lambda x: (int(x[0][1:]), x[0][0])):
            if case.aretes:
                aretes_str = ", ".join(f"{a.sommet_arrive} ({a.orientation})" for a in case.aretes)
            else:
                aretes_str = "—"
            print(f"{nom:>4} → {aretes_str}")
        
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
    def coup_possible(self, depart):
        

        piece = self.sommets[depart].piece

        if piece == None:
            return []
        elif piece == 'tour':
            return self.coup_possible_tour(depart)
        elif piece == 'fou':
            return self.coup_possible_fou(depart)
        elif piece == 'dame':
            return self.coup_possible_dame(depart)
        elif piece == 'cavalier':
            return self.coup_possible_cavalier(depart)
        elif piece == 'roi':
            return self.coup_possible_roi(depart)
        elif piece == 'pion':
            return self.coup_possible_pion(depart)
        else:
            print("Erreur : pièce inconnue.")
            return []

#tour
    def coup_possible_tour_lettre(self,actuel,couleur,deja_vu,est_initial=False):
        if actuel in deja_vu:

            return [];
        deja_vu.append(actuel);

        list_coup = []

        if est_initial:
            for coup_potentiel in self.sommets[actuel].voisin_arete_tour_par_lettre():
                list_coup += self.coup_possible_tour_lettre(coup_potentiel,couleur,deja_vu)
        elif self.sommets[actuel].piece is None :
            list_coup.append(actuel);
            for coup_potentiel in self.sommets[actuel].voisin_arete_tour_par_lettre():
                list_coup += self.coup_possible_tour_lettre(coup_potentiel,couleur,deja_vu)
        elif self.sommets[actuel].piece is not None and self.sommets[actuel].couleur == couleur:
            list_coup+=[];
        elif self.sommets[actuel].piece is not None and self.sommets[actuel].couleur != couleur:
            list_coup.append(actuel);
        return list_coup;
        
    def coup_possible_tour_chiffre(self,actuel,couleur,deja_vu,est_initial=False):
        if actuel in deja_vu:
            return [];
        deja_vu.append(actuel);

        list_coup = []

        if est_initial:
            for coup_potentiel in self.sommets[actuel].voisin_arete_tour_par_chiffre():
                list_coup += self.coup_possible_tour_chiffre(coup_potentiel,couleur,deja_vu)
        elif self.sommets[actuel].piece is None :
            list_coup.append(actuel);
            for coup_potentiel in self.sommets[actuel].voisin_arete_tour_par_chiffre():
                list_coup += self.coup_possible_tour_chiffre(coup_potentiel,couleur,deja_vu)
        elif self.sommets[actuel].piece is not None and self.sommets[actuel].couleur == couleur:
            list_coup+=[];
        elif self.sommets[actuel].piece is not None and self.sommets[actuel].couleur != couleur:
            list_coup.append(actuel);
        return list_coup;

    def coup_possible_tour(self,depart):
        couleur = self.sommets[depart].couleur

        coups = self.coup_possible_tour_chiffre(depart,couleur,[],est_initial=True);
        coups += self.coup_possible_tour_lettre(depart,couleur,[],est_initial=True);
        return coups

#fou
    def coup_possible_fou_a1(self, actuel,couleur,deja_vu,est_initial=False):
        if actuel in deja_vu:
            return [];
        deja_vu.append(actuel);


        list_coup = []

        if self.sommets[actuel].piece is None and not est_initial:
            list_coup.append(actuel);
            for coup_potentiel in self.sommets[actuel].voisin_arete_fou_a1():
                list_coup += self.coup_possible_fou_a1(coup_potentiel,couleur,deja_vu)
        elif self.sommets[actuel].piece is not None and self.sommets[actuel].couleur == couleur and not est_initial:
            list_coup += [];
        elif self.sommets[actuel].piece is not None and self.sommets[actuel].couleur != couleur:
            list_coup.append(actuel);
        else: #est_initial == True
            for coup_potentiel in self.sommets[actuel].voisin_arete_fou_a1():
                list_coup += self.coup_possible_fou_a1(coup_potentiel,couleur,deja_vu)
        return list_coup;
    
    def coup_possible_fou_h1(self, actuel,couleur,deja_vu,est_initial=False):
        if actuel in deja_vu:
            return [];
        deja_vu.append(actuel);


        list_coup = []

        if self.sommets[actuel].piece is None and not est_initial:
            list_coup.append(actuel);
            for coup_potentiel in self.sommets[actuel].voisin_arete_fou_h1():
                list_coup += self.coup_possible_fou_h1(coup_potentiel,couleur,deja_vu)
        elif self.sommets[actuel].piece is not None and self.sommets[actuel].couleur == couleur and not est_initial:
            list_coup += [];
        elif self.sommets[actuel].piece is not None and self.sommets[actuel].couleur != couleur:
            list_coup.append(actuel);
        else: #est_initial == True
            for coup_potentiel in self.sommets[actuel].voisin_arete_fou_h1():
                list_coup += self.coup_possible_fou_h1(coup_potentiel,couleur,deja_vu)
        return list_coup;

    def coup_possible_fou(self,depart):
        couleur = self.sommets[depart].couleur

        coups = self.coup_possible_fou_a1(depart,couleur,[],est_initial=True);
        coups += self.coup_possible_fou_h1(depart,couleur,[],est_initial=True);
        return coups

    def coup_possible_dame(self, depart):
        couleur = self.sommets[depart].couleur

        coups = [];
        
        coups += self.coup_possible_tour_lettre(depart,couleur,[],est_initial=True);
        coups += self.coup_possible_tour_chiffre(depart,couleur,[],est_initial=True);
        coups += self.coup_possible_fou_a1(depart,couleur,[],est_initial=True);
        coups += self.coup_possible_fou_h1(depart,couleur,[],est_initial=True);
        return coups
    
    def coup_possible_roi(self, depart):

        coups = self.sommets[depart].voisin_arete_tour_par_chiffre();
        coups += self.sommets[depart].voisin_arete_tour_par_lettre();
        coups += self.sommets[depart].voisin_arete_fou_a1();
        coups += self.sommets[depart].voisin_arete_fou_h1();    

        #enlever les coups où il y a une pièce de la même couleur
        coups2=[];
        for coup in coups:
            if not( self.sommets[coup].piece is not None and self.sommets[coup].couleur == self.sommets[depart].couleur ):
                coups2.append(coup)
        coups=coups2

        # ---------  cas du roque
        couleur = self.sommets[depart].couleur
        #roque à gauche possible
        if self.peut_roquer[couleur][0]: 
            if couleur ==0 and self.sommets['b1'].piece is None and self.sommets['c1'].piece is None and self.sommets['d1'].piece is None and self.sommets['a1'].piece == 'tour' and self.sommets['a1'].couleur == couleur :
                coups.append('c1')
            elif couleur ==1 and self.sommets['i8'].piece is None and self.sommets['j8'].piece is None and self.sommets['k8'].piece is None and self.sommets['l8'].piece == 'tour' and self.sommets['l8'].couleur == couleur:
                coups.append('j8')
            elif couleur ==2 and self.sommets['e12'].piece is None and self.sommets['f12'].piece is None and self.sommets['g12'].piece is None and self.sommets['h12'].piece == 'tour' and self.sommets['h12'].couleur == couleur:
                coups.append('f12')
        #roque à droite possible
        if self.peut_roquer[couleur][1]:
            if couleur ==0 and self.sommets['f1'].piece is None and self.sommets['g1'].piece is None and self.sommets['h1'].piece == 'tour' and self.sommets['h1'].couleur == couleur :
                coups.append('g1')
            elif couleur ==1 and self.sommets['b8'].piece is None and self.sommets['c8'].piece is None and self.sommets['a8'].piece == 'tour' and self.sommets['a8'].couleur == couleur:
                coups.append('b8')
            elif couleur ==2 and self.sommets['j12'].piece is None and self.sommets['k12'].piece is None and self.sommets['l12'].piece == 'tour' and self.sommets['l12'].couleur == couleur:
                coups.append('k12')

        return coups
    
    #cavalier
    def coup_possible_cavalier_ccl(self, depart):
        voisins1 = self.sommets[depart].voisin_arete_tour_par_chiffre();

        voisins2 = []
        for v in voisins1:
            voisins2 = list(set(( self.sommets[v].voisin_arete_tour_par_chiffre()) + voisins2))
        voisins2.remove(depart)

        voisins3 = []
        for v in voisins2:
            voisins3 += self.sommets[v].voisin_arete_tour_par_lettre()

        return voisins3
    
    def coup_possible_cavalier_llc(self, depart):
        voisins1 = self.sommets[depart].voisin_arete_tour_par_lettre();

        voisins2 = []
        for v in voisins1:
            voisins2 = list(set(( self.sommets[v].voisin_arete_tour_par_lettre()) + voisins2))
        voisins2.remove(depart)

        voisins3 = []
        for v in voisins2:
            voisins3 += self.sommets[v].voisin_arete_tour_par_chiffre()

        return voisins3
    
    def coup_possible_cavalier_cll(self, depart):
        voisins1 = self.sommets[depart].voisin_arete_tour_par_chiffre();
        voisins2 = []
        for v in voisins1:
            voisins2 += self.sommets[v].voisin_arete_tour_par_lettre() 
        voisins3 = []
        for v in voisins2:
            voisins3 = list(set(( self.sommets[v].voisin_arete_tour_par_lettre()) + voisins3))
        
        for v in voisins1:
            if v in voisins3:
                voisins3.remove(v)
        
        return voisins3
    
    def coup_possible_cavalier_lcc(self, depart):
        voisins1 = self.sommets[depart].voisin_arete_tour_par_lettre();
        voisins2 = []
        for v in voisins1:
            voisins2 += self.sommets[v].voisin_arete_tour_par_chiffre() 
        voisins3 = []
        for v in voisins2:
            voisins3 = list(set(( self.sommets[v].voisin_arete_tour_par_chiffre()) + voisins3))
        
        for v in voisins1:
            if v in voisins3:
                voisins3.remove(v)
        
        return voisins3
        
    def coup_possible_cavalier(self, depart):
        coups = self.coup_possible_cavalier_ccl(depart);
        coups = list(set(coups + self.coup_possible_cavalier_llc(depart)));
        coups = list(set(coups + self.coup_possible_cavalier_cll(depart)));
        coups = list(set(coups + self.coup_possible_cavalier_lcc(depart)));

        #verifier que les coups sont valides (case vide ou case occupée par une pièce adverse)
        couleur = self.sommets[depart].couleur

        coups2 = [];
        for coup in coups:
            if not (self.sommets[coup].piece is not None and self.sommets[coup].couleur == couleur):
                coups2.append(coup)
        coups = coups2

        return coups;

    #pion
    def coup_possible_pion_blanc(self, depart):
        lettre=str(depart[0])
        chiffre=int(depart[1:])

        liste_coups=[]
        #----------------on ajoute les coups potentiels
        #----cas ou on avance 
        liste_coups_avance=[]
        #cas où le pion est sur sa position initiale
        if chiffre==2 and self.sommets[lettre+'3'].piece is None:
            liste_coups_avance.append(lettre+str(chiffre+2))
        #cas avancer d'une case
        liste_coups_avance += self.sommets[depart].voisin_arete_tour_par_lettre()
        #verification que la case est libre
        for coup in liste_coups_avance:
            if self.sommets[coup].piece is None:
                liste_coups.append(coup)
        
        #----cas ou on mange
        liste_coups_mange=[]
        liste_coups_mange += self.sommets[depart].voisin_arete_fou_a1()
        liste_coups_mange += self.sommets[depart].voisin_arete_fou_h1()
        #verification que la case est occupée par une pièce adverse
        for coup in liste_coups_mange:
            if self.sommets[coup].piece is not None and self.sommets[coup].couleur !=0:
                liste_coups.append(coup)
            elif coup == self.prise_en_passant[1] or coup == self.prise_en_passant[2]: #prise en passant
                liste_coups.append(coup)
        
        #----------------on filtre les coups qui reculent
        coups2=[];
        for coup in liste_coups:
            chiffre_coup=int(coup[1:])
            if not(chiffre_coup <= chiffre):
                coups2.append(coup)
        liste_coups=coups2
                
        return liste_coups

    def coup_possible_pion_rouge(self, depart):
        lettre=str(depart[0])
        chiffre=int(depart[1:])

        liste_coups=[]
        #----------------on ajoute les coups potentiels
        #----cas ou on avance 
        liste_coups_avance=[]
        #cas où le pion est sur sa position initiale
        if chiffre==7 and self.sommets[lettre+'6'].piece is None:
            liste_coups_avance.append(lettre+'5')
        #cas avancer d'une case
        liste_coups_avance += self.sommets[depart].voisin_arete_tour_par_lettre()
        #verification que la case est libre
        for coup in liste_coups_avance:
            if self.sommets[coup].piece is None:
                liste_coups.append(coup)
        
        #----cas ou on mange
        liste_coups_mange=[]
        liste_coups_mange += self.sommets[depart].voisin_arete_fou_a1()
        liste_coups_mange += self.sommets[depart].voisin_arete_fou_h1()
        #verification que la case est occupée par une pièce adverse
        for coup in liste_coups_mange:
            if self.sommets[coup].piece is not None and self.sommets[coup].couleur !=1:
                liste_coups.append(coup)
            elif coup == self.prise_en_passant[0] or coup == self.prise_en_passant[2]: #prise en passant
                liste_coups.append(coup)
        
        #----------------on filtre les coups qui reculent
        liste_des_coups_a_retirer=[];
        for coup in liste_coups:
            chiffre_coup=int(coup[1:])
            if chiffre in {9,10,11,12}:
                if chiffre_coup < chiffre:
                    liste_des_coups_a_retirer.append(coup)
            elif chiffre == 5:
                if chiffre_coup == 6:
                    liste_des_coups_a_retirer.append(coup)
            else :
                if chiffre_coup >= chiffre:
                    liste_des_coups_a_retirer.append(coup)

        for coup in liste_des_coups_a_retirer:
            liste_coups.remove(coup)

        
        return liste_coups
    
    def coup_possible_pion_noir(self, depart):
        lettre=str(depart[0])
        chiffre=int(depart[1:])

        liste_coups=[]
        #----------------on ajoute les coups potentiels
        #----cas ou on avance 
        liste_coups_avance=[]
        #cas où le pion est sur sa position initiale
        if chiffre==11 and self.sommets[lettre+'10'].piece is None:
            liste_coups_avance.append(lettre+'9')
        #cas avancer d'une case
        liste_coups_avance += self.sommets[depart].voisin_arete_tour_par_lettre()
        #verification que la case est libre
        for coup in liste_coups_avance:
            if self.sommets[coup].piece is None:
                liste_coups.append(coup)
        
        #----cas ou on mange
        liste_coups_mange=[]
        liste_coups_mange += self.sommets[depart].voisin_arete_fou_a1()
        liste_coups_mange += self.sommets[depart].voisin_arete_fou_h1()
        #verification que la case est occupée par une pièce adverse
        for coup in liste_coups_mange:
            if self.sommets[coup].piece is not None and self.sommets[coup].couleur !=2:
                liste_coups.append(coup)
            elif coup == self.prise_en_passant[0] or coup == self.prise_en_passant[1]: #prise en passant
                liste_coups.append(coup)
        
        #----------------on filtre les coups qui reculent
        liste_des_coups_a_retirer=[];
        for coup in liste_coups:
            chiffre_coup=int(coup[1:])
            if chiffre in {6,7,8}:
                if chiffre_coup < chiffre:
                    liste_des_coups_a_retirer.append(coup)
            elif chiffre ==5:
                if chiffre_coup == 9:
                    liste_des_coups_a_retirer.append(coup)
            else:
                if chiffre_coup >= chiffre:
                    liste_des_coups_a_retirer.append(coup)
        for coup in liste_des_coups_a_retirer:
            liste_coups.remove(coup)
        return liste_coups

    def coup_possible_pion(self, depart):
        couleur = self.sommets[depart].couleur

        if couleur ==0:
            return self.coup_possible_pion_blanc(depart)
        elif couleur ==1:
            return self.coup_possible_pion_rouge(depart)
        else:
            return self.coup_possible_pion_noir(depart)




#------Initialisation du plateau------
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
