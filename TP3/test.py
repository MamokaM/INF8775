
# def create_middle_zone(sorted_subset):
   
#     enclo = list(sorted_subset.keys())[0] # get biggest enclo
#     size = list(sorted_subset.values())[0] # get size of biggest enclo
#     # print(enclo) 
#     # print(size) 

#     zone_size = math.ceil(math.sqrt(size)) # find middle zone size
#     # print(size)
    
#     nb_row = math.floor(size/zone_size)
#     nb_col =  size - (nb_row * zone_size)
#     # print(nb_row)
#     # print(nb_col)

#     zone = np.zeros((zone_size,zone_size))
#     # print(zone)
#     zone[0:nb_row,:] = enclo
#     zone[nb_row:nb_row+1,0:nb_col] = enclo
#     return zone
    
# def create_theme_zone(sorted_subset):

#     # create middle zone
#     middle_zone = create_middle_zone(sorted_subset)
#     print(middle_zone)

#     # create theme zone matrix
#     print(len(sorted_subset))
#     zone_size = middle_zone.shape[0] + 2*len(sorted_subset)-1
#     print(zone_size)
#     zone = np.zeros((zone_size,zone_size))
#     print(zone)

#     # insert middle zone in matrix
#     center = zone_size//2
#     print('center',center)
#     delta = int(middle_zone.shape[0] /2) +1
#     print('delta',delta)
#     index = center - delta
#     print(index)
#     zone[index:index+middle_zone.shape[0],index:index+middle_zone.shape[0]] = middle_zone
#     print(zone)

#     # populate zone 
#     for i, (enclo, size) in enumerate(sorted_subset.items()):
        
#         if i == 0: continue # dont take into consideration the first enclo (already computed)
   
       
#     #     for j in range(size):
#     #         print(i,j)
#     #         print(abs(center - i))
#     #         print(abs(center - j))
#     #         #if (i+index<zone_size and  j+index<zone_size):
#     #         zone[i+index,j+index] = max(abs(center - (i+index)), abs(center - (j+index)))

#     # print(zone)


# def verification_zone(coordinate,k):
#     combs_theme = combinations(coordinate,2)
#     for paire in combs_theme:
#         lenght = distance(paire[0][0], paire[0][1], paire[1][0], paire[1][0])
#         if lenght > k :
#             print(paire)
#             print("oop bigger than")
#             break;