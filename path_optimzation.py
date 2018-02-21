# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 21:23:57 2017

@author: Alexis Le Chapelain
"""

# -----------------------------------------------------------------------------
# 
#                                  Exercise 
# 
# -----------------------------------------------------------------------------

"""
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
"""

# -----------------------------------------------------------------------------
# Import packages
# -----------------------------------------------------------------------------

import numpy as np

# -----------------------------------------------------------------------------
# Declare functions
# -----------------------------------------------------------------------------

def build_graph(my_list):
    '''
    Build a weighted directed acyclic graph (DAG) representing the possible consumer paths.
    Each element of the data structure 'edgelist' is a list with the number of the origin node, 
    and tuples containing the destination node, and the weight associated to it. 
    Argument :
        - my_list : a list representing a problem to solve, and whose first element is a numpy array with the values 
                    of the offers.
    Return :
        - edgelist : a list of edges associated to each vertex in mylist, and representing a directed graph
    '''
    # Extract the list of offer on which we have to find an optimal path
    my_array = my_list[0]
    # Add the last element to be reached. Set at 0 to avoid double counting in the computation of total performance
    my_array = np.append(my_array,0) 
    # get the lenght of the array
    length_array=len(my_array)
    
    ## Set graph
    edgelist=[]
     # loop on all the vertice in the array 
    for j in range(length_array):           
        edgelist_temp=[]
        # loop on all the possible edge from a given vertex ; range(5) because we can skip at most four offers
        for i in range(5): 
            # This condition ensures that we do not try to reach an edge outside of the array (could be more elegant, I know)
            if (i+1 + j < length_array): 
                # build the tuple : the destination node i+1+j (starting node index=j and we add i+1 to reach a new node), 
                # and its value my_array[i + j+1 ]. 
                edge = (i+1 + j, my_array[i + j+1 ])
                # Add to the list of tuples
                edgelist_temp.append(edge)
        # Add the index of the origin vertex to the list of tuples describing the destination vertice
        templist = [j] + edgelist_temp
        edgelist.append(templist)
    return edgelist

                
def dag_shortest_path(my_graph):
    '''
    Algorithm computing the shortest past on the graph through the predecessor subgraph (see Cormen et al. for details).
    Basically, for each node, we compute its least costly predecessor, ie. the previous from which it is reachable,
    and which is the less costly. From it, we compute the optimal path and its cost.
    Argument :
        - my_graph : a directed acyclic graph as build by the function "build_graph"
    Return :
        - my_solution : a list containing the total cost of the path, and the list of the node forming the path. 
    '''
    # Get the number of vertice
    num_vertice = len(my_graph)
    
    # Initialization of the predecessor subgraph
    myvertice = []
    for i in range(num_vertice):
        myvertice.append([i,9999,9999])
    myvertice[0][1]=0
    
    ##  building the predecessor subgraph
    
    # loop on the vertice ; -1 because the last vertex has no related (directed) edge
    for i in range(num_vertice-1):  
        # for a given vertice, loop on all the related edges
        for j in range(len(my_graph[i])-1): 
            # +1 because first index of the list is for the id of the vertice
            j=j+1  
            graph_destination_node = my_graph[i][j][0]
            graph_destination_node_value = my_graph[i][j][1]
            # Check condition to see if the new path is less costly the previous one. 
            # If yes, we replace it
            if  myvertice[graph_destination_node][1] > myvertice[i][1]  - graph_destination_node_value :  
                myvertice[graph_destination_node][1] = myvertice[i][1]  - graph_destination_node_value
                myvertice[graph_destination_node][2] = i
                
    ##  obtaining the path selected by the algorithm and its cost
    
    stop = 999
    # initiate local as the first predecessor in the graph (starting from the end), and cost_path as its cost
    local = myvertice[num_vertice-1][2]
    cost_path = myvertice[num_vertice-1][1] 
    coordinate_path = []
    # The loop goes backward along the graph, stocking the vertice along the way
    while stop > 0: 
        coordinate_path.append(local) 
        local = myvertice[local][2] # we update the current node
        cost_path =+ myvertice[local-1][1] # update the cost
        stop = local # we stop when we reach the beginning of the path. 
        
    my_solution = [cost_path,coordinate_path]
            
    return my_solution
    

def main_function(my_array):
    """
    Main function: iterate on the array. As long as it can reach positive values, it add them to the path and add their
    values to the total value. When it can reach only negative values, it creates a problem, and turn it into a directed
    acyclic graph. Then, it solves the problem by finding the shortest path, and return the path and its cost. 
    Argument : 
        - my_array : a numpy array with numerical values
    Return : 
        - consumer_path : all the offer ID and their associated relevance
        - total_relevance : the total relevance achieved
    """
    
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
                total_relevance = total_relevance - my_solution[0] # update total relevance ; nb: minus because the output of the algorithm is a cost
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

array_to_optimize = np.random.randint(-8,2,10000)

#  my_results[0] returns the optimal offer serie, while my_results[1] returns 
# the maximum relevance attainable. 

consumer_path,total_relevance = main_function(array_to_optimize)


print("The maximum relevance which can be reached is " + str(total_relevance) + ".")
        
        
  

