#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 14:25:14 2020

@author: mariapereda
"""

from hierarchical_bipartite import hierarchical_bipartite

## Hobbies dataset

#Data from https://github.com/cran/FactoMineR
read_file = pd.read_csv('hobbies.csv', dtype='category')  # read file 
data = read_file.loc[:,'Reading':'Fishing'] # select columns (features) we want 
tvdata= read_file.loc[:,'TV']
tv_dummies = pd.get_dummies(tvdata, prefix='TV', prefix_sep='_')

#Uncomment to include 'Sex' as feature
sex = read_file['Sex'] #Uncoment to include "sex" as variable
sex1=pd.get_dummies(sex)
#data['sex']= sex1.iloc[:,0] #F=1 M=0

labels1=(list(data.axes[1]))
labels=[i+'_1' for i in labels1]+[i+'_0' for i in labels1]+list(tv_dummies.axes[1])

X=data.as_matrix().astype(int)
X = X.T
notA=np.ones(X.shape)-X
X=np.concatenate((X,notA))

data2 = tv_dummies.T
X=np.concatenate((X,data2))

results = hierarchical_bipartite(X,labels,plot=True,indexes=True, xFontSize=8)

#results[1].savefig('Hobbies_dendogram_withSex.pdf',dpi=900)
#results[3].savefig('hobbies_cvis_withSex.pdf',dpi=900)
results[1].savefig('Hobbies_dendogram.pdf',dpi=900)
results[3].savefig('hobbies_cvis.pdf',dpi=900)