import random
import math
import copy
from itertools import combinations
from itertools import permutations

# function to read coordinate points of a file, 
# put them in a list 
# and return the list 
def readFile(file):
    points = []
    f = open(file, "r")
    lines = f.readlines()
    for i in range (1,len(lines)):
        lst = lines[i].strip().split()
        points.append([eval(i) for i in lst])
    return points

def display(initialP, algoResult):
    result = [initialP.index(i) for i in algoResult]
    print("result before concatenation", result)
    index_0 = result.index(0)
    result_0 = result[index_0:] + result[1:index_0+1]
    if result_0[1] > result_0[len(result_0)-2] : result_0.reverse()
    print("result after concatenation ",result_0)

# greedy
def greedy(points):
    s = []
    nb_points = len(points)
    nb = random.randint(0,nb_points-1)
    firstPoint = points[nb]
    s.append(firstPoint)
    points.remove(firstPoint)
    while ( len(points)!=0 ):
        min = float('inf')
        minPoint = []
        for point in points:
            distance = round(math.dist(s[len(s)-1], point))
            if (distance < min) :
                min = distance
                minPoint = point
        s.append(minPoint)
        points.remove(minPoint)
    s.append(firstPoint)
    return s      

# dynamic programmation
def dynProg(points): 

    # matrix of distances
    dis = [[round(math.dist(points[i], points[j])) for j in range(len(points))] for i in range(len(points))] 

    # list of vertices to find combination
    vertex = []
    for i in range(1,len(points)):
        vertex.append(i)

    # list of all possible combinations
    final_comb = []
    for num in range(0, len(points)-1):
        combination = list(combinations(vertex,num))
        final_comb += combination

    # dict of S, i and D[i][s]
    D = {j: {i: float('inf') for i in range(1,  len(points))} for j in final_comb}
   
    min_path_dis = float('inf')
    final_path = (0,) 

    # calculate D[S][i]
    for S in D:
        for i in D[S]:
            if len(S)==0:
                D[S][i] = dis[0][i]
            else:
                min = float('inf')
                for j in S:
                    if (dis[i][j]==0):
                        min = None
                    elif (min and (dis[i][j] + D[tuple(s for s in S if s != j)][j] < min)) :
                        min = dis[i][j] + D[tuple(s for s in S if s != j)][j] 
                D[S][i] = min
            
            # find final path
            if (len(S)== len(points)-2) and (D[S][i]!=None):
                min_path_dis = dis[1][i]+D[S][i]
                final_path = (0,)+ (i,) + S +(0,)

    return final_path           

def MST(points):
    result = []
    result.append(points[0])
    points.remove(points[0])
    tree = []

    while(len(points)!=0):
        min_dis = float("inf")
        start =[]
        end=[]
        for i in range(0,len(result)) :
                for j in range(0,len(points)):
                    distance =  round(math.dist(result[i], points[j]))
                    if distance < min_dis:
                        min_dis=distance
                        start = result[i]
                        end = points[j]
        result.append(end)
        points.remove(end)
        tree.append((start,end,min_dis))

    print(tree)
    return(tree)

def approx_algo(points):

    #mst
    mst_tree = MST(points)

    #random vertex
    nb = random.randint(0,len(points)-1)

    root = mst[nb]
    binary_tree = {}









            










####### Greedy results #######
# initialPoints = readFile("n5_0")
# print("Initial points :",initialPoints)

# greedy_result = greedy(initialPoints)
# print("greedy :", greedy_result)

# # display 
# initialPoints = readFile("n5_0")
# display(initialPoints,greedy_result)

####### Dynamic prog #######
# initialPoints = readFile("N5_0")
# print("Initial points :",initialPoints)
# dynProg_result = dynProg(initialPoints)
# print("dynamic prog :",dynProg_result)


####### Approximating prog #######

totalPoints = readFile("n5_0")
print("points :", totalPoints)
MST(totalPoints)



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
