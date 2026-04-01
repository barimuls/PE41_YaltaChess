from Plateau import *
from FonctionJeux import *

# Classe pour gérer les différentes parties et modes de jeu
class Gestionnaire_de_jeu :
    def __init__(self):
        self._plateau = Plateau()
        
class Partie(Gestionnaire_de_jeu):
    def __init__(self, joueurs , est_en_ligne = False):
        super().__init__()
        assert isinstance(joueurs, list) and len(joueurs) == 3, "joueurs doit être une liste de 3 éléments"
        assert all(isinstance(joueur, Joueur) for joueur in joueurs), "Tous les éléments de joueurs doivent être des instances de la classe Joueur"
        self.__joueurs = joueurs  # [joueur0, joueur1, joueur2] , potentiellement IA ou humain
        assert isinstance(est_en_ligne, bool), "est_en_ligne doit être un booléen"
        self.__est_en_ligne = est_en_ligne
        
        # initialiser le plateau de jeu
        self._plateau.creer_plateau_yalta()
        self._plateau.remplir_arete()
        self._plateau.remplir_pieces_initiales()
    
    def tour_de_jeu(self, couleur):
        self._plateau.afficher()
        coup =  self.__joueurs[couleur].choisir_coup(self._plateau)
        assert coup is not None, "Le joueur doit choisir un coup valide"
        
        jouer_le_coup(self._plateau, coup[0], coup[1], self.__joueurs[couleur].get_couleur())
    
        #verifier la condition de victoire
        if verifier_victoire(self._plateau, couleur):
            print(f"Le joueur {couleur} a gagné !")
            return 
        else:
            self.tour_de_jeu((couleur + 1) % 3)  # passer au joueur suivant
        
        
class Mode_personnalise(Gestionnaire_de_jeu): # pour les tutoriels 
    def __init__(self , est_en_ligne = False):
        super().__init__()
        assert isinstance(est_en_ligne, bool), "est_en_ligne doit être un booléen"
        self.__est_en_ligne = est_en_ligne
        
# classes pour les différents types de joueurs (humain ou IA)
class Joueur:
    def __init__(self, couleur):
        assert couleur in [0,1,2], "La couleur doit être 0, 1 ou 2"
        self.__couleur = couleur
        
    def get_couleur(self):
        return self.__couleur
    
class Joueur_humain(Joueur):
    def __init__(self, couleur):
        super().__init__(couleur)
    
class Joueur_humain_console(Joueur_humain):
    def __init__(self, couleur):
        super().__init__(couleur)
        
    def choisir_coup(self, plateau):
        print (f"C'est le tour du joueur {self.get_couleur()}.");
        depart = input ("Entrez la case de départ : ");
        arrivee = input ("Entrez la case d'arrivée : ");
        #vérifier la validité du coup
        if not coup_est_valide(plateau, depart, arrivee, self.get_couleur()):
            print("Coup invalide. Veuillez réessayer.")
            return self.choisir_coup(plateau)
        
        return (depart, arrivee)

class Joueur_IA(Joueur):
    def __init__(self, couleur):
        super().__init__(couleur)
     
def lancer_partie(joueurs, est_en_ligne = False):
    partie = Partie(joueurs, est_en_ligne)
    partie.tour_de_jeu(0) # le joueur 0 commence
   
        
if __name__ == "__main__":
    joueur_0 = Joueur_humain_console(0)
    joueur_1 = Joueur_humain_console(1)
    joueur_2 = Joueur_humain_console(2)
    joueurs = [joueur_0, joueur_1, joueur_2]
    
    lancer_partie(joueurs, est_en_ligne = False)
