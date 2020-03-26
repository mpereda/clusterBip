#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 12:03:40 2020

@author: mariapereda
"""

import pandas as pd
from hierarchical_bipartite_color import hierarchical_bipartite_color


# We load the adjacency matrix of the original network
datos = pd.read_csv('Zackary_original.csv', dtype='int', sep=',', header=None)  # read file 
labels1=[str(i+1) for i in range(datos.shape[0])]

#We set the principal diagonal to ones

for i in range(len(datos)):
    for j in range(len(datos[i])):  
        if i==j:
            datos[i][j]=1

# The dataset need to have categorical variables
datos=datos.astype('category')

# We load the ground truth (partition we want to use to color the entities labels)
clusters = pd.read_csv('zachary_gt.txt', dtype='int', sep=' ', delimiter='\t', header=None) #red original Zackary
gt = dict(zip(labels1, clusters[0]))


#We apply the algorithm
results = hierarchical_bipartite_color(datos,labels1,gt, plot=True,indexes=True, xFontSize=8)


results[1]
results[3]