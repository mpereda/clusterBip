#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 23:14:05 2019

@author: Ignacio
"""
import networkx as nx
import numpy as np


def random_bipartite(num_features, num_entities, p0 = 0.5, p_rewiring=0):
    
    # p0 : Probability for edge creation
    # p_rewiring: 0 => no links, 1=> all links; p = p0 for complete random
    
    num_entities = int(num_entities/2)
    num_features = int(num_features/2)

    A = nx.bipartite.random_graph(num_features, num_entities, p0)
    bottom_nodes_A, top_nodes_A = nx.bipartite.sets(A)
    A_bimatrix =  nx.bipartite.biadjacency_matrix(A,row_order=list(top_nodes_A),
                                                  column_order=list(bottom_nodes_A)).toarray()

    # Create Random Bipartite B:
    B = nx.bipartite.random_graph(num_features, num_entities, p0)
    bottom_nodes_B, top_nodes_B = nx.bipartite.sets(B)
    B_bimatrix =  nx.bipartite.biadjacency_matrix(B,row_order=list(top_nodes_B),
                                                  column_order=list(bottom_nodes_B)).toarray()
                                                
    # Set probability of cross links
    from_A_to_B = np.random.binomial(1, p_rewiring,size=(num_entities,num_features))
    from_B_to_A = np.random.binomial(1, p_rewiring,size=(num_entities,num_features))

                                                
    G_bimatrix = np.block([[A_bimatrix,from_A_to_B],[from_B_to_A, B_bimatrix]])
          
    return G_bimatrix
