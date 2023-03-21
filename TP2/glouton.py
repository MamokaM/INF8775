import random
import math
import copy
from itertools import combinations

# function to read coordinate points of a file, 
# put them in a list 
# and return the list 
def readFile(file):
    points = []
    f = open(file, "r")
    lines = f.readlines()
    for i in range (1,len(lines)):
        lst = lines[i].strip().split()
        #points.append((int(lst[0]),int(lst[1])))
        points.append([eval(i) for i in lst])
    
    return points

def display(initialP, algoResult):

    result = [initialP.index(i) for i in algoResult]
    print("result before concatenation", result)
    index_0 = result.index(0)
    result_0 = result[index_0:] + result[1:index_0+1]
    if result_0[1] > result_0[len(result_0)-2] : result_0.reverse()
    print("result after concatenation ",result_0)

# Greedy algo
def greedy(points):
    s = []
    nb_points = len(points)
    nb = random.randint(0,nb_points-1)
    firstPoint = points[nb]
    s.append(firstPoint)
    points.remove(firstPoint)

    while ( len(points)!=0 ):
        min = 2000
        minPoint = []
        for point in points:
            distance = round(math.dist(s[len(s)-1], point))
            #print("Distance ",distance, " between ", s[len(s)-1], " and ", point )
            if (distance < min) :
                min = distance
                minPoint = point
            
        s.append(minPoint)
        points.remove(minPoint)

    s.append(firstPoint)
    return s

def dynProg(points):
    #combinations
    final_comb = []
    for num in range(1, len(points)-2):
        
        combination = list(combinations(points,num))
        #comb_list = [list(comb) for comb in combination]
        print("combination :",combination)
        final_comb+=combination
    print("final :",final_comb)
    
    ## D[i][j]
    value = 2000
    dis = [[value for j in range(len(final_comb))] for i in range(len(points))]
    
    for i in range(len(points)):
        for j in range(0,len(final_comb)):
            print("j",j)
            if j == 0:
                print("S :",final_comb[j])
                dis[i][j] = round(math.dist(points[i], points[0])) 
            #else:
                #dis[i][j] =round(math.dist(points[i], points[j])) + dis[i][j]
    print(dis)
    


     
  
    

####### Greedy results #######
# initialPoints = readFile("n5_0")
# print("Initial points :",initialPoints)

# greedy_result = greedy(initialPoints)
# print("greedy :", greedy_result)

# # display 
# initialPoints = readFile("n5_0")
# display(initialPoints,greedy_result)


####### Dynamic prog #######
initialPoints = readFile("n5_0")
print("Initial points :",initialPoints)
dynProg(initialPoints)



# totalPoints = readFile("n5_0")
# print("points :", totalPoints)


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
