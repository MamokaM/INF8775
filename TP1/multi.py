import argparse
import numpy as np
import time



if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-a", "--algorithm", required=True, default = 0, type=str,
                        help="Define which algorithm will be used to multiply the matrices")
    parser.add_argument("-e1", "--matrix_1", required=True, type=str,
                        help="Define the name of the first matrix")
    parser.add_argument("-e2", "--matrix_2", required=True, type=str,
                        help="Define the name of the second matrix")
    parser.add_argument("-p", "--result", required=False, action ='store_true',
                        help="Define the name of the second matrix")
    parser.add_argument("-t", "--time", required=False, action ='store_true',
                        help="Define the name of the second matrix")                                            
 
    args = parser.parse_args()  
    
    algo = args.algorithm
    name_m1 = args.matrix_1
    name_m2 = args.matrix_2
    
    # algo conventionnel
    def conv(A, B):
        n = len(A)
        C = np.zeros((n,n))
        for i in range(0, n):
            for j in range(0, n):
                for k in range(0, n):
                    C[i][j] += A[i][k]*B[k][j]      
        return C

    # algo conventionnel strassen and starassen with tresholder
    def strassen(A,B, seuil=1):
        n = len(A)
        C = np.zeros((n,n))
        if n == seuil:
           
            C = conv(A, B)
        else: 
           
            A11 = A[0:int(n/2),0:int(n/2)]
            A12 = A[0:int(n/2),int(n/2):n]
            A21 = A[int(n/2):n, 0:int(n/2)] 
            A22 = A[int(n/2):n, int(n/2):n]
            B11 = B[0:int(n/2),0:int(n/2)]
            B12 = B[0:int(n/2),int(n/2):n]
            B21 = B[int(n/2):n, 0:int(n/2)] 
            B22 = B[int(n/2):n, int(n/2):n]

            M1 = strassen(A11 + A22, B11 + B22)
            M2 = strassen(A21 + A22, B11)
            M3 = strassen(A11, B12 - B22)
            M4 = strassen(A22, B21 - B11)
            M5 = strassen(A11 + A12, B22)
            M6 = strassen(A21 - A11, B11 + B12)
            M7 = strassen(A12 - A22, B21 + B22)

            C11 = M1 + M4 - M5 + M7
            C12 = M3 + M5
            C21 = M2 + M4
            C22 = M1 - M2 + M3 + M6

            C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
        
        return C

    # function to read matricies from files
    def readMatrix(file):
        matrix = []
        f = open(file, "r")
        lines = f.readlines()
        for i in range (1,len(lines)):
            lst = lines[i].strip().split()
            matrix.append([eval(i) for i in lst])
        return np.array(matrix)
    
    # read matrice A and matrice B from files
    matrix1 = readMatrix(args.matrix_1)
    matrix2 = readMatrix(args.matrix_2)

    n = len(matrix1)
    result = np.zeros((n,n))
    start = 0.0
    end=0.0

    if algo == "conv":

        start = time.time()
        result = conv(matrix1, matrix2)
        end = time.time() # calculate  execution time of algorithm

    elif algo == "strassen":
        
        start = time.time()
        result = strassen(matrix1, matrix2)
        end = time.time()

    elif algo == "strassenSeuil":

        start = time.time()
        result = strassen(matrix1, matrix2, 256)
        end = time.time()


    if args.result :
        # clean dislay of matrice 
        #https://stackoverflow.com/questions/52904487/python-numpy-2d-array-aligned-without-brackets
        for a in result:
            for elem in a:
                print("{}".format(int(elem)), end=" ")
            print(end="\n")
         
    if args.time:
        # display of execution time in ms
        print((end - start)*1000)

    
    

        

    
