# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 21:23:57 2017

@author: alechapelain
"""

# -----------------------------------------------------------------------------
# 
#                                  Exercise 
# 
# -----------------------------------------------------------------------------

# To solve the problem, the algorithm reframes it as a shortest path problem
# on a graph. It exploits the fact that the possible series of offer can be 
# represented a directed acyclic graph. The optimal serie of offer correspond
#  to the shortest (least expensive) path on the graph. This can be easily 
# found with standard algorithm. The the algoritm running time is low, bounded
# above by O(n).

# The algorithm is divided in three functions:
#    - the "build_graph" function build an adjacency matrix based on a sequence
#      of contiguous offer.
#    - the "dag_shortest_path" function finds the shortest path from the first 
#      to the last offer on this graph.
#    - the "main_function" splits the total serie of offer on sub-series to 
#      in order to efficiently compute the solution. It uses the two previous
#      function as subroutines. 

# -----------------------------------------------------------------------------
# Import packages
# -----------------------------------------------------------------------------

import numpy as np

# -----------------------------------------------------------------------------
# Declare functions
# -----------------------------------------------------------------------------

def build_graph(my_list):
    'build a weighted directed acyclic graph representing the possible consumer paths'
    my_array = my_list[0]
    my_array = np.append(my_array,0) 
    length_array=len(my_array)
    
    #Set graph
    edgelist=[]
    for j in range(length_array):   # loop on all the vertice         
        edgelist_temp=[]
        for i in range(5): # loop on all the possible edge from a vertice ; range(5) because we can skip at most for offers
            if (i+1 + j < length_array):
                edge = [i+1 + j, my_array[i + j+1 ]]
                edgelist_temp.append(edge)
        templist = [j] + edgelist_temp
        edgelist.append(templist)
    return edgelist

                
def dag_shortest_path(my_graph):
    'Algorithm computing the shortest past through the predecessor subgraph'
    num_vertice = len(my_graph)
    
    # Initializationof the predecessor subgraph
    myvertice = []
    for i in range(num_vertice):
        myvertice.append([i,9999,9999])
    myvertice[0][1]=0
    
    # building the predecessor subgraph
    for i in range(num_vertice-1):  # loop on the vertice ; -1 because the last vertex has no related (directed) edge
        for j in range(len(my_graph[i])-1):  # for a given vertice, loop on all the related edges
            j=j+1 # because first index of the list is for id of the vertice 
            if  myvertice[my_graph[i][j][0]][1] > myvertice[i][1]  - my_graph[i][j][1] :  
                myvertice[my_graph[i][j][0]][1] = myvertice[i][1]  - my_graph[i][j][1]
                myvertice[my_graph[i][j][0]][2] = i
                
    # obtaining the path selected by the algorithm and its cost 
    stop = 999
    local = myvertice[num_vertice-1][2]
    cost_path = myvertice[num_vertice-1][1] 
    coordinate_path = []
    while stop > 0: # The loop goes backward along the shortest, stocking the vertice along the way
        coordinate_path.append(local)
        local = myvertice[local][2]
        stop = local
        
    my_solution = [cost_path,coordinate_path]
            
    return my_solution
    

def main_function(my_array):
    'Main function: '
    'Input : a numpy array with numerical values'
    'Output: a list with (1) all the offer ID and their associated relevance,'
    'and (2) the total relevance achieved'
    
    # A small twist to force the serie of proposed offer to start a the first 
    # possible one, and finish at the last possible one
    value_first_offer = my_array[0]
    value_last_offer = my_array[len(my_array)-1]
    consumer_path = []
    total_relevance = value_first_offer + value_last_offer
    my_array[0]=0 
    my_array[len(my_array)-1]=0 
    local1=0
    
    for i in range(len(my_array)):  # loop on the entire array
        
        if my_array[i]>-1:          # if the relevance of an offer is positive
            consumer_path.append([i,my_array[i]])  # add this offer to the consumer path...
            total_relevance=total_relevance+my_array[i]  # ...and increase the total relevance by the offer amount
            local2 = i
            
            if abs(local2-local1)>5:  # test if the distance to the previous positive offer higher than 5
                my_problem = [my_array[local1:local2],local1,local2] # if yes, set problem to be solved, by retrieving the associated array of offer
                my_graph = build_graph(my_problem)  # build graph associated to the problem
                my_solution = dag_shortest_path(my_graph)  # find shortest path
                total_relevance = total_relevance - my_solution[0] # update total relevance ; nb: minus because the ouptut of the algorithm is a cost
                for k in range(len(my_solution[1])):   # retrieve the index used in the solution path and add them to the complete consumer path
                    consumer_path.append([my_solution[1][k]+local1,my_problem[0][my_solution[1][k]]])
                
            local1=local2
    
    # fix the potential problem at the beginning and the end of the serie (if values are negative)
    consumer_path[0][1]=value_first_offer
    consumer_path[len(consumer_path)-1][1]=value_last_offer
    
    results = [consumer_path,total_relevance]
    return results
        

        
# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

# create random array to be optimized on

array_to_optimize = np.random.random_integers(-8,2,1000)

#  my_results[0] returns the optimal offer serie, while my_results[1] returns 
# the maximum relevance attainable. 

my_results = main_function(array_to_optimize)


print("The maximum relevance which can be reached is " + str(my_results[1]) + ".")
        
        
  

