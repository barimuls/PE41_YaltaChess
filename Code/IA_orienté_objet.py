
# je lance un projet de transformation des fonctions IA en programation orientée objet
# l'idée c'est de faire une ia pour un joueur en particulier, qui agira à son tour en fonction de l'ia choisie

from abc import ABC, abstractmethod
import copy
import random
from Plateau import Graph

class AbstractIA(ABC): # le ABC sert a utiliser abstractmethod, qui permet de forcer les classes filles à implémenter la méthode choisir_coup, sinon ça renvoie une erreur
    """Classe abstraite pour toutes les IA"""
    
    def __init__(self, couleur):
        self.__couleur = couleur
    
    @property
    def couleur(self):     
        return self.__couleur
    @couleur.setter
    def couleur(self, value):
        self.__couleur = value
        
    @abstractmethod # si choisir_coup n'est pas implémenté dans une classe fille, ça renvoie une erreur
    def choisir_coup(self, plateau):
        """Méthode abstraite à implémenter par chaque IA"""
        pass
    
    def coups_possibles(self, plateau):
        """Récupère tous les coups possibles pour cette IA, de la forme : liste de [case , liste de case d'arrivée possibles]"""
        liste_coups = []
        for case, sommet in plateau.sommets.items():
            if sommet is not None and sommet.couleur == self.couleur:
                coups = plateau.coup_possible(case)
                if coups:
                    liste_coups.append([case, coups])
        return liste_coups
    


class IAAleatoire(AbstractIA):
    """IA qui joue des coups aléatoires, renvoie None si aucun coup n'est possible, sinon renvoie un tuple (case_depart, case_arrivee)"""
    
    def choisir_coup(self, plateau):
        """Choisit un coup aléatoire parmi les coups possibles de la forme (case_depart, case_arrivee)"""
        liste_coups = self.coups_possibles(plateau)
        
        if not liste_coups:
            return None
        
        n = random.randint(0, len(liste_coups) - 1)
        case_depart = liste_coups[n][0]
        m = random.randint(0, len(liste_coups[n][1]) - 1)
        case_arrivee = liste_coups[n][1][m]
        
        return (case_depart, case_arrivee)

#IA heuristique est une IA min_max de profondeur 1
class IAMinimax(AbstractIA):
    """IA utilisant l'algorithme Minimax"""
    
    def __init__(self, couleur, profondeur=2, evaluateur=None, optimise=False):
        super().__init__(couleur)
        self.profondeur = profondeur
        self.evaluateur = evaluateur if evaluateur else EvaluateurSimple()
        self.optimise = optimise  # Utilise déjouer au lieu de deepcopy
    
    def choisir_coup(self, plateau):
        if self.optimise:
            return self._minimax_optimise(plateau)
        else:
            return self._minimax_standard(plateau)
    
    def _minimax_standard(self, plateau):
        """Minimax avec deepcopy"""
        resultat = self._evaluation_recursive(plateau, self.couleur, self.profondeur)
        return (resultat[3], resultat[4])
    
    def _minimax_optimise(self, plateau):
        """Minimax avec déjouer"""
        plateau_copie = copy.deepcopy(plateau)
        resultat = self._evaluation_recursive_optimise(plateau_copie, self.couleur, self.profondeur)
        return (resultat[3], resultat[4])
    
    def _evaluation_recursive(self, plateau, couleur, profondeur):
        """Évaluation récursive avec deepcopy"""
        if profondeur == 0:
            scores = [self.evaluateur.evaluer(plateau, c) for c in [0, 1, 2]]
            return scores + [None, None]
        
        liste_coups = self.coups_possibles_pour_couleur(plateau, couleur)
        
        meilleur_score = -float('inf')
        meilleur_coup = None
        
        for coup in liste_coups:
            depart = coup[0]
            for arrivee in coup[1]:
                plateau_copie = copy.deepcopy(plateau)
                self._jouer_coup_couleur(plateau_copie, couleur, depart, arrivee)
                
                evaluation = self._evaluation_recursive(plateau_copie, (couleur + 1) % 3, profondeur - 1)
                
                heuristic = self._calculer_heuristique(evaluation, couleur)
                
                if heuristic > meilleur_score:
                    meilleur_score = heuristic
                    meilleur_coup = (evaluation[0], evaluation[1], evaluation[2], depart, arrivee)
        
        return meilleur_coup
    
    def _evaluation_recursive_optimise(self, plateau, couleur, profondeur):
        """Évaluation récursive avec déjouer"""
        if profondeur == 0:
            scores = [self.evaluateur.evaluer(plateau, c) for c in [0, 1, 2]]
            return scores + [None, None]
        
        liste_coups = self.coups_possibles_pour_couleur(plateau, couleur)
        
        meilleur_score = -float('inf')
        meilleur_coup = None
        
        for coup in liste_coups:
            depart = coup[0]
            for arrivee in coup[1]:
                self._jouer_coup_couleur(plateau, couleur, depart, arrivee)
                
                evaluation = self._evaluation_recursive_optimise(plateau, (couleur + 1) % 3, profondeur - 1)
                
                heuristic = self._calculer_heuristique(evaluation, couleur)
                
                if heuristic > meilleur_score:
                    meilleur_score = heuristic
                    meilleur_coup = (evaluation[0], evaluation[1], evaluation[2], depart, arrivee)
                
                self._dejouer_coup_couleur(plateau, couleur, depart, arrivee)
        
        return meilleur_coup
    
    def _calculer_heuristique(self, evaluation, couleur):
        """Calcule l'heuristique à partir de l'évaluation"""
        return (evaluation[couleur] - 
                0.5 * evaluation[(couleur + 1) % 3] - 
                0.5 * evaluation[(couleur + 2) % 3])
    
    def coups_possibles_pour_couleur(self, plateau, couleur):
        """Récupère les coups possibles pour une couleur donnée"""
        liste_coups = []
        for case, sommet in plateau.sommets.items():
            if sommet is not None and sommet.couleur == couleur:
                coups = plateau.coup_possible(case)
                if coups:
                    liste_coups.append([case, coups])
        return liste_coups
    
    def _jouer_coup_couleur(self, plateau, couleur, depart, arrivee):
        """Helper pour jouer un coup"""
        from FonctionJeux import jouer_le_coup
        jouer_le_coup(plateau, couleur, depart, arrivee)
    
    def _dejouer_coup_couleur(self, plateau, couleur, depart, arrivee):
        """Helper pour déjouer un coup"""
        from FonctionJeux import dejouer_le_coup
        dejouer_le_coup(plateau, couleur, depart, arrivee)          
    
class Evaluateur(ABC):
    """Classe abstraite pour l'évaluation de position"""
    
    VALEURS_PIECES = {
        'pion': 1,
        'cavalier': 3,
        'fou': 5,
        'tour': 3,
        'dame': 9,
        'roi': 1000
    }
    
    VALEURS_PIECES_V1 = {
        'pion': 1,
        'cavalier': 3.1,
        'fou': 3.6,
        'tour': 4.6,
        'dame': 7.8,
        'roi': 1000
    }
    
    MATE_SCORE = 10**9
    
    @abstractmethod
    def evaluer(self, plateau, couleur):
        """Évalue la position pour une couleur donnée"""
        pass
    
    def score_materiel(self, plateau, couleur, valeurs=None):
        """Calcule le score matériel"""
        if valeurs is None:
            valeurs = self.VALEURS_PIECES
            
        score = 0
        for case, sommet in plateau.sommets.items():
            if sommet.piece is not None and sommet.couleur == couleur:
                score += valeurs[sommet.piece]
        return score
    
    def roi_present(self, plateau, couleur):
        """Vérifie si le roi est présent"""
        for case, sommet in plateau.sommets.items():
            if sommet.couleur == couleur and sommet.piece == 'roi':
                return True
        return False
    
    def trouver_roi(self, plateau, couleur):
        """Trouve la position du roi"""
        for case, sommet in plateau.sommets.items():
            if sommet is not None and sommet.piece == 'roi' and sommet.couleur == couleur:
                return case
        return None
    
class EvaluateurSimple(Evaluateur):
    """Évaluateur basique basé uniquement sur le matériel"""
    
    def evaluer(self, plateau, couleur):
        score_joueur = self.score_materiel(plateau, couleur)
        score_adv1 = self.score_materiel(plateau, (couleur + 1) % 3)
        score_adv2 = self.score_materiel(plateau, (couleur + 2) % 3)
        
        return score_joueur - 0.5 * score_adv1 - 0.5 * score_adv2   
    
class EvaluateurComplet(Evaluateur):
    """Évaluateur avancé avec mobilité, pression, sécurité du roi"""
    
    def __init__(self, coef_mobilite=0.05, coef_pression=0.5):
        self.coef_mobilite = coef_mobilite
        self.coef_pression = coef_pression
    
    def evaluer(self, plateau, couleur):
        # Vérifier si le roi est présent
        if not self.roi_present(plateau, couleur):
            return -self.MATE_SCORE
        
        # Vérifier si on peut capturer un roi ennemi
        if self._peut_capturer_roi_ennemi(plateau, couleur):
            return self.MATE_SCORE
        
        # Vérifier si notre roi est menacé
        if self._roi_menace(plateau, couleur):
            return -4
        
        # Calculer les composantes du score
        score = 0
        score += self.score_materiel(plateau, couleur, self.VALEURS_PIECES_V1)
        score += self._score_mobilite(plateau, couleur)
        score += self._score_pression(plateau, couleur)
        score += self._score_securite_roi(plateau, couleur)
        
        return score
    
    def _score_mobilite(self, plateau, couleur):
        """Calcule le score de mobilité"""
        mobilite = 0
        for case, sommet in plateau.sommets.items():
            if sommet.piece is not None and sommet.couleur == couleur:
                mobilite += len(plateau.coup_possible(case))
        return self.coef_mobilite * mobilite
    
    def _score_pression(self, plateau, couleur):
        """Calcule la pression sur les pièces adverses"""
        pression = 0
        for case, sommet in plateau.sommets.items():
            if sommet is not None and sommet.couleur != couleur and sommet.piece is not None:
                # Si on peut capturer cette pièce
                for case2, sommet2 in plateau.sommets.items():
                    if sommet2 is not None and sommet2.couleur == couleur:
                        if case in plateau.coup_possible(case2):
                            pression += self.coef_pression
                            break
        return pression
    
    def _peut_capturer_roi_ennemi(self, plateau, couleur):
        """Vérifie si on peut capturer un roi ennemi"""
        for case, sommet in plateau.sommets.items():
            if sommet is not None and sommet.couleur == couleur:
                for coup in plateau.coup_possible(case):
                    cible = plateau.sommets[coup]
                    if cible is not None and cible.piece == 'roi':
                        return True
        return False
    
    def _roi_menace(self, plateau, couleur):
        """Vérifie si le roi est menacé"""
        roi_pos = self.trouver_roi(plateau, couleur)
        if roi_pos is None:
            return False
        
        danger = 0
        for case, sommet in plateau.sommets.items():
            if sommet is not None and sommet.couleur != couleur:
                if roi_pos in plateau.coup_possible(case):
                    danger += 1
        return danger > 0
    
    def _score_securite_roi(self, plateau, couleur):
        """Évalue la sécurité du roi"""
        case_roi = self.trouver_roi(plateau, couleur)
        if case_roi is None:
            return -self.MATE_SCORE
        
        danger_total = 0
        voisins = self._cases_adjacentes_roi(plateau, case_roi)
        
        for v in voisins:
            att1 = self._nombre_attaquants(plateau, v, (couleur + 1) % 3)
            att2 = self._nombre_attaquants(plateau, v, (couleur + 2) % 3)
            def_ami = self._nombre_attaquants(plateau, v, couleur)
            
            danger = 0
            danger += self._danger_attaquants(att1)
            danger += self._danger_attaquants(att2)
            
            if att1 > 0 and att2 > 0:
                danger += 3
            
            danger -= min(def_ami, 2)
            
            if plateau.sommets[v].piece is not None and plateau.sommets[v].couleur == couleur:
                danger += 1
            
            danger_total += danger
        
        return -danger_total
    
    def _cases_adjacentes_roi(self, plateau, case_roi):
        """Récupère les cases adjacentes au roi"""
        voisins = set()
        sommet = plateau.sommets[case_roi]
        voisins |= set(sommet.voisin_arete_tour_par_chiffre())
        voisins |= set(sommet.voisin_arete_tour_par_lettre())
        voisins |= set(sommet.voisin_arete_fou_a1())
        voisins |= set(sommet.voisin_arete_fou_h1())
        return voisins
    
    def _nombre_attaquants(self, plateau, case, couleur):
        """Compte le nombre d'attaquants d'une case"""
        n = 0
        for c, s in plateau.sommets.items():
            if s.piece is not None and s.couleur == couleur:
                if case in plateau.coup_possible(c):
                    n += 1
        return n
    
    @staticmethod
    def _danger_attaquants(n):
        """Calcule le danger en fonction du nombre d'attaquants"""
        if n <= 0:
            return 0
        if n == 1:
            return 2
        if n == 2:
            return 4
        return 5   

class GestionnaireJeu:
    """Gère le déroulement d'une partie"""
    
    def __init__(self, plateau, joueurs):
        """
        :param plateau: Le plateau de jeu
        :param joueurs: Liste de 3 joueurs (humain ou IA)
        """
        self.__plateau = plateau
        self.__joueurs = joueurs  # [joueur0, joueur1, joueur2]
        self.__joueur_actuel = 0
    
    @property
    def plateau(self):
        return self.__plateau
    @plateau.setter
    def plateau(self, value):
        assert isinstance(value, Graph), "Le plateau doit être une instance de Graph"
        self.__plateau = value
        
    @property
    def joueurs(self):
        return self.__joueurs
    @joueurs.setter
    def joueurs(self, value):
        assert isinstance(value, list) and len(value) == 3, "Il doit y avoir exactement 3 joueurs"
        self.__joueurs = value
        
    @property
    def joueur_actuel(self):
        return self.__joueur_actuel
    @joueur_actuel.setter
    def joueur_actuel(self, value):
        assert isinstance(value, int) and 0 <= value < 3, "L'indice du joueur doit être entre 0 et 2"
        self.__joueur_actuel = value
    
    def jouer_tour(self, depart=None, arrivee=None):
        """
        Joue un tour pour le joueur actuel
        :param depart: Case de départ (pour joueur humain)
        :param arrivee: Case d'arrivée (pour joueur humain)
        :return: (victoire, joueur_gagnant, depart, arrivee)
        """
        joueur = self.joueurs[self.joueur_actuel]
        
        if isinstance(joueur, JoueurHumain):
            if depart is None or arrivee is None:
                return (None, None, None, None)  # Attente d'input
            
            if not self._coup_valide(depart, arrivee):
                return (False, None, None, None)
            
            coup = (depart, arrivee)
        else:  # IA
            coup = joueur.choisir_coup(self.plateau)
            if coup is None:
                return (True, self.joueur_actuel, None, None)  # Pas de coup possible = défaite
        
        # Jouer le coup
        self._jouer_coup(coup[0], coup[1])
        
        # Vérifier victoire
        if self._verifier_victoire():
            return (True, self.joueur_actuel, coup[0], coup[1])
        
        # Passer au joueur suivant
        self.joueur_actuel = (self.joueur_actuel + 1) % 3
        
        return (None, None, coup[0], coup[1])
    
    def jouer_partie_complete(self, mode='console'):
        """
        Joue une partie complète
        :param mode: 'console' ou 'web'
        """
        if mode == 'console':
            return self._jouer_partie_console()
        else:
            raise ValueError("Mode web nécessite une interface web")
    
    def _jouer_partie_console(self):
        """Joue une partie en mode console"""
        self.plateau.afficher()
        
        while True:
            joueur = self.joueurs[self.joueur_actuel]
            
            print(f"\nC'est le tour du joueur {self.joueur_actuel}")
            
            if isinstance(joueur, JoueurHumain):
                depart = input("Entrez la case de départ : ")
                arrivee = input("Entrez la case d'arrivée : ")
            else:
                print(f"L'IA {type(joueur).__name__} réfléchit...")
                coup = joueur.choisir_coup(self.plateau)
                depart, arrivee = coup
                print(f"L'IA joue : {depart} → {arrivee}")
            
            victoire, gagnant, _, _ = self.jouer_tour(depart, arrivee)
            
            if victoire is False:
                print("Coup invalide. Veuillez réessayer.")
                continue
            
            self.plateau.afficher()
            
            if victoire:
                print(f"\n🎉 Le joueur {gagnant} a gagné la partie!")
                break
    
    def _coup_valide(self, depart, arrivee):
        """Vérifie si un coup est valide"""
        from FonctionJeux import coup_est_valide
        return coup_est_valide(self.plateau, depart, arrivee, self.joueur_actuel)
    
    def _jouer_coup(self, depart, arrivee):
        """Joue un coup"""
        from FonctionJeux import jouer_le_coup
        jouer_le_coup(self.plateau, self.joueur_actuel, depart, arrivee)
    
    def _verifier_victoire(self):
        """Vérifie si le joueur actuel a gagné"""
        from FonctionJeux import verifier_victoire
        return verifier_victoire(self.plateau, self.joueur_actuel)

class JoueurHumain:
    """Représente un joueur humain"""
    
    def __init__(self, couleur):
        self.couleur = couleur
    
