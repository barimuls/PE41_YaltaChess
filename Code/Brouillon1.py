# a mettre dans la classe Graphe

def arete_diaga1(self, case):
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

    ar = []
    lettre = 'abcdefghijkl'

    def index(L, x):
        for i in range(len(L)):
            if L[i] == x:
                return i

    ind = index(lettre, case.nom[0])
    case2 = lettre[ind+1]+str(int(case.nom[1:])+1)
    case1 = lettre[ind-1]+str(int(case.nom[1:])-1)

def gagnant(plateau,joueur) :
    if verifier_victoire(plateau,joueur)
    return joueur
