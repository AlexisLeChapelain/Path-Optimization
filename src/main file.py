# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 14:20:01 2018

@author: Alexis Le Chapelain

Main file

"""
import os 
import numpy as np
import matplotlib.pyplot as plt

os.chdir("Data/Path")

from path_optimization import PathOptimisation

# A small simulation to show how the total relevance depends on the lenght of the gap allowed 
array_to_optimize = np.random.randint(-50,2,10000)
length_simul = 50
list_of_result = []
for i in range(1,length_simul+1):
    optim =  PathOptimisation(max_gap = i)
    consumer_path,total_relevance = optim.main_function(array_to_optimize)
    list_of_result.append(total_relevance)
    print("The maximum relevance which can be reached is " + str(total_relevance) + ".")
    
abscisse = list(range(1,length_simul+1))
fig, ax = plt.subplots()
ax.plot(abscisse,list_of_result)
plt.show()
        
# Another simulation to show the variance of the results when we simulate different arrays
length_simul = 500
list_of_result = []
for i in range(length_simul):
    optim =  PathOptimisation(max_gap = 10)
    array_to_optimize = np.random.randint(-20,2,10000)
    consumer_path,total_relevance = optim.main_function(array_to_optimize)
    list_of_result.append(total_relevance)

num_bins = 20
fig, ax = plt.subplots()
n, bins, patches = ax.hist(list_of_result, num_bins, normed=1)
plt.show()


