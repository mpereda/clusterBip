#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 14:47:23 2020

@author: mariapereda
"""
import pandas as pd
from hierarchical_bipartite_color import hierarchical_bipartite_color

datos = pd.read_csv('zachary_A_diagonal.csv', dtype='category', sep=';', header=None)  # read file 
labels1=[str(i+1) for i in range(datos.shape[0])]

# We load the ground truth (partition we want to use to color the entities labels)
clusters = pd.read_csv('zachary_gt.txt', dtype='int', sep=' ', delimiter='\t', header=None) #red original Zackary
gt = dict(zip(labels1, clusters[0]))

results = hierarchical_bipartite_color(datos,labels1,gt, plot=True,indexes=True, xFontSize=8)


results[1]
results[3]
