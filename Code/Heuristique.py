from math import inf

class Heuristique: 
    def __init__(sel):
        pass

class par_valeur(Heuristique):
    def __init__(self, valeur_piece = {'pion':1,'cavalier':3.1,'fou':3.6,'tour':4.6,'dame':7.8,'roi': inf}):
        super().__init__()
        self.valeur_piece = valeur_piece
        
    def score_joueur(self, plateau, joueur):
        score = 0;
        for case in plateau.sommets.items():
        if plateau.sommets[case[0]].piece != None:
            if plateau.sommets[case[0]].couleur == joueur:
                score += self.valeur_piece[plateau.sommets[case[0]].piece];
        return score;
    
