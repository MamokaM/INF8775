import random
import math
import copy
from itertools import combinations
from itertools import permutations
import argparse
import time

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a",
        "--algorithm",
        required=True,
        default=0,
        type=str,
        help="Define which algorithm will be used",
    )
    parser.add_argument(
        "-e", "--graph", required=True, type=str, help="Define the path of the graph"
    )
    parser.add_argument(
        "-p",
        "--result",
        required=False,
        action="store_true",
        help="Display indexes of path",
    )
    parser.add_argument(
        "-t",
        "--time",
        required=False,
        action="store_true",
        help="Display algorithm time",
    )

    args = parser.parse_args()
    algo = args.algorithm
    graph_name = args.graph

    # greedy
    def greedy(points):
        s = []
        nb_points = len(points)
        nb = random.randint(0, nb_points - 1)
        firstPoint = points[nb]
        s.append(firstPoint)
        points.remove(firstPoint) # O(n)
        while len(points) != 0: # O(n)
            min = float("inf")
            minPoint = []
            for point in points: # O(n)
                distance = round(math.dist(s[len(s) - 1], point))
                if distance < min:
                    min = distance
                    minPoint = point
            s.append(minPoint)
            points.remove(minPoint) # O(n)
        s.append(firstPoint)
        return s

    # dynamic programmation
    def dynProg(points):

        # matrix of distances O(n^2)
        dis = [
            [round(math.dist(points[i], points[j])) for j in range(len(points))]
            for i in range(len(points))
        ]

        # list of vertices to find combination O(n)
        vertex = []
        for i in range(1, len(points)):
            vertex.append(i)

        # list of all possible combinations O(2^n)
        final_comb = []
        for num in range(0, len(points) - 1):
            combination = list(combinations(vertex, num))
            final_comb += combination

        # dict of S, i and D[i][s] O(2^n)
        D = {j: {i: float("inf") for i in range(1, len(points))} for j in final_comb}

        min_path_dis = float("inf")
        final_path = (0,)

        # calculate D[S][i] 
        for S in D : # O(2^n), car le nombre de sous-ensembles possibles d'un ensemble n est 2^n
            for i in D[S] : # O(n), car on itère sur chaque sommet                                                      
                if len(S) == 0:                                                     
                    D[S][i] = dis[0][i]                                             
                else:
                    min = float("inf")                                              
                    for j in S: # O(n), car on itère sur chaque sommet                                                     
                        if dis[i][j] == 0:
                            min = None
                        elif min and (
                            dis[i][j] + D[tuple(s for s in S if s != j)][j] < min
                        ):
                            min = dis[i][j] + D[tuple(s for s in S if s != j)][j]
                    D[S][i] = min

                # find final path
                if (
                    (len(S) == len(points) - 2)
                    and (D[S][i] != None)
                    and dis[1][i] + D[S][i] < min_path_dis
                ):
                    min_path_dis = dis[1][i] + D[S][i]
                    final_path = (0,) + (i,) + S + (0,)
        return final_path

    def findEdges(vertices):
        edges = []
        for row in vertices:
            for col in vertices:
                if row != col:
                    edge = (row, col, round(math.dist(row[1], col[1])))
                    invEdge = (col, row, round(math.dist(row[1], col[1])))
                    if edge not in edges and invEdge not in edges:
                        edges.append((row, col, round(math.dist(row[1], col[1]))))
        return edges

    # A utility function to find set of an element i
    # (truly uses path compression technique)
    # From : https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/
    def findParent(parent, i):
        # Reassignment of node's parent
        # to root node as
        # path compression requires
        if parent[i] != i:
            parent[i] = findParent(parent, parent[i])
        return parent[i]

    # A function that does union of two sets of x and y
    # (uses union by rank)
    # From : https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/
    def union(parent, rank, x, y):

        # Attach smaller rank tree under root of
        # high rank tree (Union by Rank)
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x

        # If ranks are same, then make one as root
        # and increment its rank by one
        else:
            parent[y] = x
            rank[x] += 1

    # The main function to construct MST
    # using Kruskal's algorithm
    # From : https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/
    def kruskalMST(points,edges):

        # This will store the resultant MST
        result = []

        # Vertices
        # vertices = []
        # index = 0
        # for point in points:
        #     vertices.append((index, point))
        #     index = index + 1

        # Edges
        #edges = findEdges(vertices)

        # An index variable, used for sorted edges
        i = 0

        # An index variable, used for result[]
        e = 0

        # Sort all the edges in non-decreasing order of their weight
        edges = sorted(edges, key=lambda item: item[2])

        parent = []
        rank = []

        for node in vertices:
            parent.append(node[0])
            rank.append(0)

        # Number of edges to be taken is less than to vertices
        while e < len(vertices) - 1:

            # Pick the smallest edge and increment
            # the index for next iteration
            u, v, w = edges[i]
            i = i + 1
            x = findParent(parent, u[0])
            y = findParent(parent, v[0])

            # If including this edge doesn't
            # cause cycle, then include it in result
            # and increment the index of result
            # for next edge
            if x != y:
                e = e + 1
                result.append([u, v, w])
                union(parent, rank, x, y)

            minimumCost = 0
            for u, v, weight in result:
                minimumCost += weight
            
        return result


    # Inspired by :
    # https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/
    # https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/
    def preOrder(mst, start, visited=None):

        # Create a set to store visited vertices
        if visited is None:
            visited = []
        
        # Mark the current node as visited
        # and print it
        visited.append(start)

        for edge in mst:

            if edge[0] == start and edge[1] not in visited:
                preOrder(mst, edge[1], visited)
            elif edge[1] == start and edge[0] not in visited:
                preOrder(mst, edge[0], visited)

        return visited

    # approximative
    def approx(points,edges):
        
        mstResult = kruskalMST(points,edges)
        # select random starting point
        startIndex = random.randint(0, len(points)-2)
        preOrderResult = preOrder(mstResult, mstResult[startIndex][0])
        preOrderResult.append(preOrderResult[0])
 
        return preOrderResult

    # function to read coordinate points of a file,
    # put them in a list
    # and return the list
    def readFile(file):
        points = []
        f = open(file, "r")
        lines = f.readlines()
        for i in range(1, len(lines)):
            lst = lines[i].strip().split()
            points.append([eval(i) for i in lst])
        return points

    def displayGreedy(initialP, algoResult):
        result = [initialP.index(i) for i in algoResult]
        index_0 = result.index(0)
        result_0 = result[index_0:] + result[1 : index_0 + 1]
        if result_0[1] > result_0[len(result_0) - 2]:
            result_0.reverse()
        return result_0

    ##### display with script #####

    # read graph from file
    graph = readFile(graph_name)

    # initialise time variables
    start = 0.0
    end = 0.0

    result = []

    if algo == "glouton":

        start = time.time()
        result_greedy = greedy(graph)
        end = time.time()  # calculate  execution time of algorithm

        graph = readFile(graph_name)
        result = displayGreedy(graph, result_greedy)

    elif algo == "progdyn":

        start = time.time()
        result = dynProg(graph)
        end = time.time()

    elif algo == "approx":
        vertices = []
        index = 0
        for point in graph:
            vertices.append((index, point))
            index = index + 1
        edges = findEdges(vertices)
        start = time.time()
        result_approx = approx(graph,edges)
        end = time.time()
        result = [tupl[0] for tupl in result_approx]
        if result[1] > result[len(result) - 2]:
            result.reverse()
        
        # total_dis = 0
        # for i in range(len(result_approx)-3):  
        #     total_dis+= round(math.dist(result_approx[i][1], result_approx[i+1][1]))
        # print(total_dis)    

    if args.result:
        ## display
        for vertex in result:
            print(vertex)



    if args.time:
        # display of execution time in ms
        print((end - start) * 1000)


