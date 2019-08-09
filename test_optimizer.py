# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 15:10:53 2018

@author: Alexis Le Chapelain
"""

import pandas as pd
import pytest

from path_optimization import PathOptimisation

 
class TestAlgo:
    
    
    def setup_method(self):
        # Define test sample
        sample = [0,-10,-10,-10,-3,-10,-10,-10,-2,-10,-10,-10,-10,-10,1,2,3]
        
        # Write optimal solution for gap = 6
        optimal_path = [0,4,8,14,15,16]
        optimal_path = pd.DataFrame(optimal_path,columns=["NodeIndex"])
        self.optimal_path = optimal_path.sort_values(by="NodeIndex")
        
        # Write solution from PathOptimisation
        gap =6
        optimizer = PathOptimisation(gap)
        consumer_path,total_relevance = optimizer.main_function(sample)
        consumer_path = pd.DataFrame(consumer_path,columns=["NodeIndex","Cost"])
        self.consumer_path = consumer_path.sort_values(by="NodeIndex").reset_index(drop=True)
        
        
    def test_path_length(self):
        """
        Test if path has the right lenght
        """
        assert self.consumer_path.shape[0]==6
        
        
    def test_optimisation_path(self):
        """
        Test if path is identical 
        """
        if self.consumer_path.shape[0]==6:
            myboolean = (self.optimal_path.NodeIndex - self.consumer_path.NodeIndex) != 0
            myboolean = myboolean.sum()
            assert myboolean==0
