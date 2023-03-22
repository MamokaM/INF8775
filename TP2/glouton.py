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
        min = float('inf')
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



# def dynProg(points):

#     ### ÉTAPE 1: DÉFINITION DU TABLEAU
#     #combinations
#     final_comb = []
#     for num in range(1, len(points)-2):
#         combination = list(combinations(points,num))
#         #comb_list = [list(comb) for comb in combination]
#         print("combination :",combination)
#         final_comb+=combination
#     print("final :",final_comb)
    
#     ## D[i][j]
#     value = float('inf')
#     dis = [[value for j in range(len(final_comb))] for i in range(len(points))]
    
    
#     for j in range(0,len(final_comb)-1):
#         print("S :",final_comb[j])
#         for i in range(0,len(points)-1):
#             if j == 0:
#                 dis[i][j] = round(math.dist(points[i], points[0])) 
#             #else:
#                 #dis[i][j] = round(math.dist(points[i], points[j])) + dis[i][j]
#     print(dis)

#     ### ÉTAPE 2 : DÉFINITION DE LA RÉCURRENCE
#     def recc(i = [], S = [], k = []):
#         D = 0
#         if len(S) == 0 :
#             D = round(math.dist(i, k))
#         else :
#             j = findMin(i, S)
#             Dij = round(math.dist(i, j))
#             S.remove(j)
#             recc(j, S, k)
#         return D

#     def findMin(i = [], S = []):
#         j = []
#         min = float('inf')
#         for point in S : 
#             dist = round(math.dist(i, point))
#             if (dist < min):
#                 min = dist
#                 j = point
#         return j

# def dynProg(points): 

#     # matrix of distances
#     dis = [[round(math.dist(points[i], points[j])) for j in range(len(points))] for i in range(len(points))] 
#     print(dis) 

#     # list of vertices to find combination
#     vertex = []
#     for i in range(1,len(points)):
#         vertex.append(i)
#     #print(vertex)

#     # list of all possible combinations
#     final_comb = []
#     for num in range(0, len(points)-1):
#         combination = list(combinations(vertex,num))
#         #comb_list = [list(comb) for comb in combination]
#         #print("combination :",combination)
#         final_comb+=combination
#     #print("final :",final_comb)

#     # dict of i, S and D[i][s]
#     D ={i: {j: float('inf') for j in final_comb} for i in range(1, len(points))}
#     #print(D)

#     # initialize initial values
#     for i in D:
#         D[i][()]= dis[i][0]
    
#     #calculate D[i][S]
#     for i in D:
#         for S in D[i]:
#             # if len(S)==0:
#             #     D[i][S]= dis[i][0]
#             # else:
#             if len(S)!=0:
#                 min = float('inf')
#                 for j in S :
#                     # print("S :",S)
#                     # print("i",i)
#                     # print("j :",j)
#                     # print("S-j :",tuple(s for s in S if s != j))
#                     # print(dis[i][j], " ", D[j][tuple(s for s in S if s != j)], "" ,dis[i][j] + D[j][tuple(s for s in S if s != j)])
#                     if (dis[i][j]==0):
#                         D[i][S] = None
#                     elif dis[i][j] + D[j][tuple(s for s in S if s != j)] < min :
#                         min = dis[i][j] + D[j][tuple(s for s in S if s != j)] 
                
#                 D[i][S] = min
                    

#     print(D)        

##### FINAL 
def dynProg(points): 

    # matrix of distances
    dis = [[round(math.dist(points[i], points[j])) for j in range(len(points))] for i in range(len(points))] 
    #print(dis) 

    # list of vertices to find combination
    vertex = []
    for i in range(1,len(points)):
        vertex.append(i)
    #print(vertex)

    # list of all possible combinations
    final_comb = []
    for num in range(0, len(points)-1):
        combination = list(combinations(vertex,num))
        final_comb+=combination
    #print("final :",final_comb)

    # dict of S, i and D[i][s]
    D = {j: {i: float('inf') for i in range(1,  len(points))} for j in final_comb}
   
    min_path_dis = float('inf')
    final_path = (0,) 
    # #calculate D[S][i]
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
            
            
            

            if (len(S)== len(points)-2) and (D[S][i]!=None) and (dis[1][i]+D[S][i] <min_path_dis):
                # print(S)
                # print(i)
                # print(dis[1][i], " ",D[S][i])
                # print(dis[1][i]+D[S][i])
                min_path_dis = dis[1][i]+D[S][i]
                final_path = (0,)+ (i,) + S

   
    print(D) 
    print(final_path)           
 

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
# s=0
# result = travellingSalesmanProblem(initialPoints,s)
# print(result)



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
