import numpy as np 
import math
from itertools import combinations
import random

def readFile(file):
    n = 0
    m = 0
    k = 0
    subset = []
    #distances = []
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
                distances = np.resize(distances, (n,n))
                index = i - n - 2
                distances[index,:]= lines[i].strip().split()
                #distances.append(list(map(int, lines[i].strip().split())))
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
    #print("ZONE : ")
    #print(zone)
    return zone

def create_theme_zone(sorted_subset):
    
    nb= 4 # change code after
    zone = initialize_theme_zone(sorted_subset,nb)

    sub_zone = zone[:,nb:zone.shape[1]]
  
    for i, (enclo, size) in enumerate(sorted_subset.items()):
        
        if i == 0 : continue # firt enclo is already set in initialize_theme_zone
        
        row,col = np.argwhere(sub_zone==-1)[0]
        # print(row, col)
    
        
        rest = size - (sub_zone.shape[1]-col) 
        sub_zone[row,col:] = enclo

        if(row + 1 >= sub_zone.shape[0] or row + 2 >= sub_zone.shape[0] ):
            #sub_zone = np.resize(sub_zone, (sub_zone.shape[0]+2,sub_zone.shape[1]))
            sub_zone = np.pad(sub_zone, ((0, 2), (0, 0)), mode='constant', constant_values=-1)
            zone = np.pad(zone, ((0, 2), (0, 0)), mode='constant', constant_values=-1)

        sub_zone[row+1,:rest] = enclo

        # if we need more than 2 rows
        rest-= sub_zone.shape[1]
        if (rest>0):
            
            sub_zone[row+2,:rest] = enclo

    #print(sub_zone)
    zone[:,nb:zone.shape[1]] = sub_zone 
    #print(zone)
    return zone


def compute_both_ways(distances):
     
    both_ways = np.transpose(distances)
    both_ways = both_ways + distances
    return both_ways 

# glouton
def create_solution(distances,enclo_sizes,theme_zone,subset,n):
    #size = int(20/2)
    zone = np.full(theme_zone.shape,-1)
    ############################### sol 2 ##################
    copy_distances = np.copy(distances)
    
    placed = list(np.copy(subset))
    to_place = []
    
    for enclo in enclo_sizes.keys():
        if enclo not in placed:
            to_place.append(enclo)
    #print(to_place)

    for enclo in placed :
        copy_distances[enclo,:] = 0
        copy_distances[:,enclo] = 0
    #print(copy_distances)

    enclo_to_place = random.choice(to_place)
    #print("chosen enclo",enclo_to_place)

    while(len(placed) != n ):
        
        ###### copied from other funct
        row,col = np.argwhere(zone==-1)[0]
        # print(row, col)
        #sub_zone[row:5-row, col:5-col] = enclo
        
        size = enclo_sizes[enclo_to_place]
        rest = size - (zone.shape[1]-col) 
        zone[row,col:] = enclo_to_place

        if(row + 1 >= zone.shape[0] or row + 2 >= zone.shape[0] ):
            #sub_zone = np.resize(sub_zone, (sub_zone.shape[0]+2,sub_zone.shape[1]))
            zone = np.pad(zone, ((0, 2), (0, 0)), mode='constant', constant_values=-1)
         

        zone[row+1,:rest] = enclo_to_place

        # if we need more than 2 rows
        rest-= zone.shape[1]
        if (rest>0):
            
            zone[row+2,:rest] = enclo_to_place
        #####
        # print("ZONE",zone)

        # print("DISTANCES",copy_distances)
        next_enclo_to_place = np.argmax(copy_distances[enclo_to_place])
        # print('next enclo to place',next_enclo_to_place)

        copy_distances[enclo_to_place,:] = 0
        copy_distances[:,enclo_to_place] = 0
        # print('UPDATED DISTANCES ',copy_distances)
        
        placed.append(enclo_to_place)
        enclo_to_place = next_enclo_to_place
       

    theme_zone = np.flip(theme_zone, axis=0)
    # print(theme_zone)
    #print(zone)

    final_zone = np.concatenate((theme_zone, zone), axis=0)
    # print(final_zone)
    return(final_zone)

  
#  def create_solution(distances,enclo_sizes,theme_zone,subset): 
#       ############## sol 1
#     copy_distances = np.copy(distances)
#     placed = np.copy(subset)
#     enclo_to_place = -1
#     while(not(np.all(copy_distances == 0))):
    
#         max_index = np.unravel_index(np.argmax(distances), distances.shape)
#         print(max_index)

#         # if both are already in the theme zone
#         if(max_index[0] in placed and max_index[1] in placed ) : 
#             copy_distances[max_index[0],max_index[1]] = 0
#             copy_distances[max_index[1],max_index[0]] = 0
#             continue
        
#         elif( max_index[0]in placed and max_index[1] not in placed) :
#             enclo_to_place = max_index[1]
#             indexes_x = np.where(theme_zone == max_index[0])[0] 
#             indexes_y = np.where(theme_zone == max_index[0])[1] 
#             index = (indexes_x[np.argmax(indexes_y)],np.max(indexes_y)+1) 
#             print(index)
          
           
#         elif( max_index[0] not in placed and max_index[1] in placed): 
#             enclo_to_place = max_index[0]
        
#         else: print()# place both // break;  


def display_theme_zone(zone,supset):
    coordinates = []
    for i in supset:
        idx = np.where(zone==i)
        idx = np.column_stack((idx[0], idx[1]))
        indexes = np.array2string(np.ravel(idx))[1:-1] 
        # print(idx)
        # print(i)
        # print(indexes) 
        ## TODO delete those lines in the end
        # for row in idx : 
        #     coordinates.append(tuple(row))
    
    
    #print(coordinates)
    #return coordinates
    
def display_zone(zone,supset):
    coordinates = []
    for i in supset:
        idx = np.where(zone==i)
        idx = np.column_stack((idx[0], idx[1]))
        indexes = np.array2string(np.ravel(idx))[1:-1] 
        # print(idx)
        # print(i)
        print(indexes) 
        ## TODO delete those lines in the end
        # for row in idx : 
        #     coordinates.append(tuple(row))
    
    
    #print(coordinates)
    #return coordinates




#################### main ##############

n, m , k, subset,enclo_sizes, distances = readFile("ex_n10_m5.txt")
#n, m , k, subset,enclo_sizes, distances = readFile("n20_m15_V-74779.txt")
#n, m , k, subset,enclo_sizes, distances = readFile("n100_m50_V-8613404.txt")
#print(n, m , k, subset,enclo_sizes, distances)
#print(subset)
#print(distances)


distances = compute_both_ways(distances)
#print(distances)

sorted_enclo_sizes = sort_all(enclo_sizes)
print("sorted enclo by size",sorted_enclo_sizes)

sorted_supset = sort_subset_by_size_dict(subset,sorted_enclo_sizes)
print("sorted subset by size",sorted_supset)

theme_zone = create_theme_zone(sorted_supset)
print(theme_zone)

final_zone = create_solution(distances,enclo_sizes,theme_zone,subset,n)
print(final_zone)

### for later
display_zone(final_zone,enclo_sizes) 
# coordinates = display_zone(theme_zone,subset)














