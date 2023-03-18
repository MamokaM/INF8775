import random
import math
import copy

def readFile(file):
    points = []
    f = open(file, "r")
    lines = f.readlines()
    for i in range (1,len(lines)):
        lst = lines[i].strip().split()
        #points.append((int(lst[0]),int(lst[1])))
        points.append([eval(i) for i in lst])
    
    return points

 

def greedy(points):
    s = []
    nb_points = len(points)
    nb = random.randint(0,nb_points-1) # de 0 à 4
    s.append(points[nb])
    points.remove(points[nb])

    while ( len(points)!=0 ):
        min = 2000
        minPoint = []
        for point in points:
            distance = math.dist(s[len(s)-1], point)
            if (distance < min) :
                min = distance
                minPoint = point
            
        s.append(minPoint)
        points.remove(minPoint)

    return s
    
totalPoints = readFile("n5_0")
print(totalPoints)
s = greedy(totalPoints)
print("s :", s)

totalPoints = readFile("n5_0")
print("points :", totalPoints)


### ALGORITHME DE PROGRAMMATION DYNAMIQUE
    # Définir une fonction dynamique(n)
        # Créer un tableau de taille (n+1) pour les résultats
        # Initialiser les résultats pour les cas de base
        # Pour i allant de 2 à n : 
            # Calculer le résultat pour i
            # Stocker le résultat dans le tableau
        # Retourner le résultat pour n

### ALGORITME APPROXIMATIF (1-relatif)
    # Trier les arêtes du graphe
    # Créer un ensemble vide d'arêtes pour l'arbre sous-tendant minimum
    # Pour chaque arête e, en commençant par la plus légère : 
        # Si l'ajout de l'arête e à l'ensemble ne crée par de cycle, ajouter e à l'ensemble
        # Sinon, ignorer e
    # Retourner l'ensemble d'arêtes pour l'arbre sous-tendant minimum
