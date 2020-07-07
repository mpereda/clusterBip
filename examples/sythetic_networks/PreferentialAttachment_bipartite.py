#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 23:14:05 2019

@author: Ignacio
"""
import networkx as nx
import numpy as np


def PreferentialAttachment_bipartite(num_entities, m, p0 = 0.5, p_rewiring=0):
    
    # p0 : Probability for edge creation
    # p_rewiring: 0 => no links, 1=> all links; p = p0 for complete random
    
    num_entities = int(num_entities/2)
    #num_features = int(num_features/2)
    m2 = int(m/2)
    
    # Create Pref Atachmentment Bipartite A:
    #generate degree pref at sequence
    G = nx.barabasi_albert_graph(num_entities, m2) # configuration model
    degree_sequence = [d for n, d in G.degree()]  # degree sequence

    A = nx.algorithms.bipartite.generators.preferential_attachment_graph( degree_sequence, p0)
    bottom_nodes_A, top_nodes_A = nx.bipartite.sets(A)
    A_bimatrix =  nx.bipartite.biadjacency_matrix(A,row_order=list(top_nodes_A),
                                                  column_order=list(bottom_nodes_A)).toarray()

    # Create Pref Atachmentment Bipartite B:
    #generate a new degree pref at sequence
    G = nx.barabasi_albert_graph(num_entities, m2) # configuration model
    degree_sequence = [d for n, d in G.degree()]  # degree sequence
    B = nx.algorithms.bipartite.generators.preferential_attachment_graph( degree_sequence, p0)
    bottom_nodes_B, top_nodes_B = nx.bipartite.sets(B)
    B_bimatrix =  nx.bipartite.biadjacency_matrix(B,row_order=list(top_nodes_B),
                                                  column_order=list(bottom_nodes_B)).toarray()
    
    #Same number of features
    if B_bimatrix.shape[0] > A_bimatrix.shape[0]:
        number=B_bimatrix.shape[0]-A_bimatrix.shape[0]
        for i in range(number):
            B_bimatrix=np.delete(B_bimatrix,B_bimatrix.shape[0]-1,0)
                   
    if B_bimatrix.shape[0] < A_bimatrix.shape[0]:
        number=A_bimatrix.shape[0]-B_bimatrix.shape[0]
        for i in range(number):
            A_bimatrix=np.delete(A_bimatrix,A_bimatrix.shape[0]-1,0)
        
    num_features=B_bimatrix.shape[0]
    
                                           
    # Set probability of cross links
    from_A_to_B = np.random.binomial(1, p_rewiring,size=(num_entities,num_features))
    from_B_to_A = np.random.binomial(1, p_rewiring,size=(num_entities,num_features))

                                                
    G_bimatrix = np.block([[np.transpose(A_bimatrix),from_A_to_B],[from_B_to_A, np.transpose(B_bimatrix)]])
    G_bimatrix[G_bimatrix>1]=1   #do not return a weighted network   
    return G_bimatrix
