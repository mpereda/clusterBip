#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 14:36:02 2020

@author: mariapereda
"""

#%%   SYNTHETIC NETWORKS
import random
from random_bipartite import random_bipartite
from hierarchical_bipartite import hierarchical_bipartite

random.seed(1)
#%%

## Random Network

# Create a random network with
features = 400
entities = 100
data1 = random_bipartite(features,entities,p0=0.5,p_rewiring=0.5)
labels1=[str(i) for i in range(entities)]

results = hierarchical_bipartite(data1,labels1,plot=True,indexes=True, xFontSize=5)
results[1].savefig('Random_dendro.pdf',dpi=900)
results[3].savefig('Random_cvis.pdf',dpi=900)

#%%

## Perfectly bipartite
features = 400
entities = 100

data2 = random_bipartite(features,entities,p0=0.5,p_rewiring=0)
data2[0,int(entities-1)]=0.99 #We need to add a link between the two clusters
labels1=[str(i) for i in range(entities)]

results = hierarchical_bipartite(data2,labels1,plot=True,indexes=True, xFontSize=5)

#%%

## Fully connected network
features = 20
entities = 10

data2 = random_bipartite(features,entities,p0=1,p_rewiring=1)
labels1=[str(i) for i in range(entities)]

results = hierarchical_bipartite(data2,labels1,plot=True,indexes=True, xFontSize=5)

#%%
import random
random.seed(55)

## In Bipartite network with some rewiring
features = 400
entities = 100

data3 = random_bipartite(features,entities,p0=0.5,p_rewiring=0.28)
labels1=[str(i) for i in range(entities)]

results = hierarchical_bipartite(data3,labels1,plot=True,indexes=True, xFontSize=5)



#%% Figure 1 panel D

## Bipartite networks with several p_rewiring
from hierarchical_bipartite import hierarchical_bipartite
from statistics import mean

import random
random.seed(5)
import matplotlib.pyplot as plt
import numpy as np

features = 400
entities = 100
labels1=[str(i) for i in range(entities)]

ejes_X=[]
ejes_Y=[]
ejes_Y_errors=[]

add=0.05
ps_rewiring= list(np.arange(0,0.5+add,add))

for ps in ps_rewiring:
    medias_x=[]
    medias_y=[]
    std_y=[]
    for r in range(100):
        data3 = random_bipartite(features,entities,p0=0.5,p_rewiring=ps)
        results = hierarchical_bipartite(data3,labels1,plot=False,indexes=True, xFontSize=8)
        medias_x.append(results[2])
        medias_y.append(results[1])
    ejes_X.append(np.mean(medias_x, axis=0))
    ejes_Y.append(np.mean(medias_y, axis=0))
    ejes_Y_errors.append(np.std(medias_y, axis=0))
