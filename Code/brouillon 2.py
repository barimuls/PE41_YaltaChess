from Plateau import *

def arete_par_lettre(self):
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
        if lettre in {'e','f','g','h'}:
            if chiffre==4:
                voisins.append(lettre+str(9))
                voisins.append(lettre+str(3))
            elif chiffre==9:
                voisins.append(lettre+str(10))
                voisins.append(lettre+str(4))
    
        elif lettre in {'i','j','k','l'}:
            if chiffre==5:
                voisins.append(lettre+str(9))
                voisins.append(lettre+str(6))
            elif chiffre==9:
                voisins.append(lettre+str(5))
                voisins.append(lettre+str(10))

        else:
            voisins.append(lettre+str(chiffre+1))
            voisins.append(lettre+str(chiffre-1))
    print(voisins)
    return voisins


## test
testA2=Case('i5',None)
arete_par_lettre(testA2)

def arete_par_chiffre(self):
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
        if lettre in {'e','f','g','h'}:
            if chiffre==4:
                voisins.append(lettre+str(9))
                voisins.append(lettre+str(3))
            elif chiffre==9:
                voisins.append(lettre+str(10))
                voisins.append(lettre+str(4))
    
        elif lettre in {'i','j','k','l'}:
            if chiffre==5:
                voisins.append(lettre+str(9))
                voisins.append(lettre+str(6))
            elif chiffre==9:
                voisins.append(lettre+str(5))
                voisins.append(lettre+str(10))

        else:
            voisins.append(lettre+str(chiffre+1))
            voisins.append(lettre+str(chiffre-1))
    print(voisins)
    return voisins
