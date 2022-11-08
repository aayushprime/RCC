import sys, getopt
import pickle
import random
import os

def calcDist(thisRoute,distMatrix):
    # from city zero to first index
    distance=distMatrix[0][thisRoute[0]]
    Nm1=len(thisRoute)-1

    # Add distance from one city to the next in the list
    for i in range(Nm1):
        distance+=distMatrix[thisRoute[i]][thisRoute[i+1]]
        
    # Add from last index back to city zero    
    distance+=distMatrix[thisRoute[Nm1]][0]
    return distance

            
if __name__ == '__main__':

    # no checks for bad inputs
    weight=int(sys.argv[1])
    mylist=[int(i) for i in sys.argv[2:]]

    #read pickle file for distanceMatrix
    distFile="distance0"+sys.argv[1]+".pickle"
    rfile = open(distFile,'rb')
    matrix=pickle.load(rfile)
    rfile.close()

    
    # Calculate its round trip distance
    # in case the best_distIn was wrong
    best_dist=calcDist(mylist,matrix)

    print(int(best_dist))
    
