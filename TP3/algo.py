import numpy as np 
import math


def readFile(file):
    n = 0
    m = 0
    k = 0
    subset = []
    distances = []
    enclo_sizes = {}
    with open(file, "r") as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            if i == 0:
                n, m, k = map(int, lines[i].split())
            elif i == 1:
                subset = list(map(int, lines[i].strip().split()))
            elif i > 1 and i < n + 2 :
                index = i-2
                #TODO maybe sort enlcloses here
                enclo_sizes[index]= (int(lines[i].strip()))
            else:
                distances.append(list(map(int, lines[i].strip().split())))
    # print(n, m, k)
    # print(subset)
    # print(enclo_sizes)
    # print(distances)
    return n, m , k, subset,enclo_sizes, distances
   

def distance(x1, y1, x2, y2):
    return abs(x2-x1)+abs(y2-y1)

def sort_all(sizes):
    #https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
    enclo_sizes_sort = dict(sorted(sizes.items(),key=lambda x:x[1],reverse=True))
    return enclo_sizes_sort


def sort_subset_by_size_dict(subset,sorted_enclos):
    sorted_subset = {}
    #for s in sub :
    # TODO find a better solution
    for enclo, size in sorted_enclos.items():
        if enclo in subset:
            sorted_subset[enclo] = size
    return sorted_subset   

def initialize_theme_zone(sorted_subset,nb) : 
    enclo_0 = list(sorted_subset.keys())[0] # get biggest enclo
    size_0 = list(sorted_subset.values())[0] # get size of biggest enclo

    size_1 = list(sorted_subset.values())[1] # get  size of second biggest enclo


    row = math.ceil(size_0/nb)
    col = math.ceil(size_1/nb) + nb
    # print(row,col)
    zone = np.full((row,col),-1)
    # print(zone)

    zone[:,:1]=enclo_0
    rest = size_0 - row 
    zone[:rest,1:nb]=enclo_0
    print("ZONE : ")
    print(zone)
    return zone

def create_theme_zone(sorted_subset):
    
    nb= 1 # change code after
    zone = initialize_theme_zone(sorted_subset,nb)

    sub_zone = zone[:,nb:zone.shape[1]]
  
    for i, (enclo, size) in enumerate(sorted_subset.items()):
        
        if i == 0 : continue
        row,col = np.argwhere(sub_zone==-1)[0]
        # print(row, col)
        #sub_zone[row:5-row, col:5-col] = enclo
       
        rest = size - (sub_zone.shape[1]-col) 
        sub_zone[row,col:] = enclo
        sub_zone[row+1,:rest] = enclo

        # if we need more than 2 rows
        rest-= sub_zone.shape[1]
        if (rest>0):
            sub_zone[row+2,:rest] = enclo

        print(sub_zone)
    zone[:,nb:zone.shape[1]] = sub_zone 
    #print(zone)
    return zone



#################### main ##############

n, m , k, subset,enclo_sizes, distances = readFile("ex_n10_m5.txt")
#n, m , k, subset,enclo_sizes, distances = readFile("n20_m15_V-74779.txt")
#n, m , k, subset,enclo_sizes, distances = readFile("n100_m50_V-8613404.txt")
#print(n, m , k, subset,enclo_sizes, distances)
#print(subset)

sorted_enclo_sizes = sort_all(enclo_sizes)
print("sorted enclo by size",sorted_enclo_sizes)

sorted_supset = sort_subset_by_size_dict(subset,sorted_enclo_sizes)
print("sorted subset by size",sorted_supset)

theme_zone = create_theme_zone(sorted_supset)
print(theme_zone)












