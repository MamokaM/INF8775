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
    for i in range(1, len(lines)):
        lst = lines[i].strip().split()
        points.append([eval(i) for i in lst])
    return points


def display(initialP, algoResult):
    result = [initialP.index(i) for i in algoResult]
    print("result before concatenation", result)
    index_0 = result.index(0)
    result_0 = result[index_0:] + result[1 : index_0 + 1]
    if result_0[1] > result_0[len(result_0) - 2]:
        result_0.reverse()
    print("result after concatenation ", result_0)


# greedy
def greedy(points):
    s = []
    nb_points = len(points)
    nb = random.randint(0, nb_points - 1)
    firstPoint = points[nb]
    s.append(firstPoint)
    points.remove(firstPoint)
    while len(points) != 0:
        min = float("inf")
        minPoint = []
        for point in points:
            distance = round(math.dist(s[len(s) - 1], point))
            if distance < min:
                min = distance
                minPoint = point
        s.append(minPoint)
        points.remove(minPoint)
    s.append(firstPoint)
    return s


# dynamic programmation
def dynProg(points):

    # matrix of distances
    dis = [
        [round(math.dist(points[i], points[j])) for j in range(len(points))]
        for i in range(len(points))
    ]

    # list of vertices to find combination
    vertex = []
    for i in range(1, len(points)):
        vertex.append(i)

    # list of all possible combinations
    final_comb = []
    for num in range(0, len(points) - 1):
        combination = list(combinations(vertex, num))
        final_comb += combination

    # dict of S, i and D[i][s]
    D = {j: {i: float("inf") for i in range(1, len(points))} for j in final_comb}

    min_path_dis = float("inf")
    final_path = (0,)

    # calculate D[S][i]
    for S in D:
        for i in D[S]:
            if len(S) == 0:
                D[S][i] = dis[0][i]
            else:
                min = float("inf")
                for j in S:
                    if dis[i][j] == 0:
                        min = None
                    elif min and (
                        dis[i][j] + D[tuple(s for s in S if s != j)][j] < min
                    ):
                        min = dis[i][j] + D[tuple(s for s in S if s != j)][j]
                D[S][i] = min

            # find final path
            if (len(S) == len(points) - 2) and (D[S][i] != None):
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
def kruskalMST(points):

    # This will store the resultant MST
    result = []

    # Vertices
    vertices = []
    index = 0
    for point in points:
        vertices.append((index, point))
        index = index + 1

    # Edges
    edges = findEdges(vertices)

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
        print("Edges in the constructed MST")
        for u, v, weight in result:
            minimumCost += weight
            print("%d -- %d == %d" % (u[0], v[0], weight))
        print("Minimum Spanning Tree", minimumCost)

    return result


""" def MST(points):
    result = []
    result.append(points[0])
    points.remove(points[0])
    tree = []

    while len(points) != 0:
        min_dis = float("inf")
        start = []
        end = []
        for i in range(0, len(result)):
            for j in range(0, len(points)):
                distance = round(math.dist(result[i], points[j]))
                if distance < min_dis:
                    min_dis = distance
                    start = result[i]
                    end = points[j]
        result.append(end)
        points.remove(end)
        tree.append((start, end, min_dis))

    return tree """


def preOrder(mst, start, visited=None):
    # Inspired by :
    # https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/
    # https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/

    # Create a set to store visited vertices
    if visited is None:
        visited = []

    # Mark the current node as visited
    # and print it
    visited.append(start)
    print("Visite : ", start)

    unvisited = []
    for edge in mst:
        if edge[0] == start and edge[1] not in visited:
            preOrder(mst, edge[1], visited)
        elif edge[0] not in visited:
            unvisited.append(edge[0])

    for vertex in unvisited:
        preOrder(mst, vertex, visited)

    return visited


####### test setup #######
activateGreedy = False
activateDisplay = False
activateDynamic = False
activateApproximative = False
activateTemp = True


####### greedy #######
if activateGreedy:
    initialPoints = readFile("n5_0")
    print("Initial points :", initialPoints)
    greedResult = greedy(initialPoints)
    print("greedy :", greedResult)

####### display #######
if activateDisplay:
    initialPoints = readFile("n5_0")
    display(initialPoints, greedResult)

####### dynamic prog #######
if activateDynamic:
    initialPoints = readFile("N5_0")
    print("Initial points :", initialPoints)
    dynProgResult = dynProg(initialPoints)
    print("dynamic prog :", dynProgResult)

####### approximating prog #######
if activateApproximative:
    initialPoints = readFile("n5_0")
    print("Initial points :", initialPoints)
    startIndex = random.randint(0, len(initialPoints) - 2)
    print("Starting index : ", startIndex)
    mst = MST(initialPoints)
    print("MST : ", mst)
    print("Starting city : ", mst[startIndex])
    preOrderResult = preOrder(mst, mst[startIndex])
    print("Pre-order Result : ", preOrderResult)


####### temp #######
if activateTemp:
    initialPoints = readFile("n5_0")
    print("Initial points : ", initialPoints)
    mstResult = kruskalMST(initialPoints)
    print("MST : ", mstResult)
    preOrderResult = preOrder(mstResult, mstResult[0][0])
    print("Pre-order : ", preOrderResult)
