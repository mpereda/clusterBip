#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hierarchical clustering of bipartite data sets based on the statistical significance of coincidences

@author: Ignacio Tamarit, Maria Pereda, Jose A. Cuesta

"""



from scipy.stats import fisher_exact
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from matplotlib import pyplot as plt
import warnings
import matplotlib.colors as colors
import matplotlib.cm as mplcm
from scipy.cluster import hierarchy



def hierarchical_bipartite_color(A, my_labels, gt, indexes=True, threshold='Susceptibility', plot=True, xFontSize=10.):
    """
        Parameters
        ----------
        A : ndarray
            binary matrix to cluster. Items to be clustered as rows, features as columns
            
        labels : list
            Labels of the items to be clustered, to be shown in the dendrogram 
        
        indexes: bool, optional
            True, compute three clustering validity indexes to select the best dendrogram cut (default is True)

        threshold : str or numeric
            If numeric: threshold to cut the dendrogram
            else:
                It will use the threshold where normalized Susceptibility is maximum
        
        plot: bool, optional
            If True, plots the dendrogram resulting from the clustering at the selected threshold

        xFontSize: numeric, optional
            x axis labels font size for the dengrogram plot (default is 10.)


        Returns
        -------
        tuple
        
        if plot==True and indexes==True:
            Returns a 4 element tuple: list of clustering membership, fig of dedrogram plot, CVIs, fig of CVIs plot
 
        if plot==False and indexes==True:
            Returns list of clustering membership, CVIs
        	
        if plot==False and indexes==False:
            urns list of clustering membership
        """
    

    
    warnings.filterwarnings("ignore")
    
    def _normalizedSusceptibility(membership):
        """ Computes normalized susceptibility cluster validity index
            """

    
        def _membershipToComponents(membership):
            """ Converts a cluster membership list to a list of components
                """
            
            components=[]
            for i in range(max(membership)):
                indices=np.where(membership == i+1)[0]
                components.append(set(indices))
            return components
    
        def _compute_suceptibility(list_of_components):
            """ Computes normalized susceptibility cluster validity index. Computed over all the components BUT the largest.
                """
            
            sizes = []
            for component in list_of_components:
                size = float(len(component))
                sizes.append(size)
        
            susc = [sizes.count(value)*(value**2) for value in set(sizes)] 
            return sum(susc)
  
        CC = _membershipToComponents(membership) # convert membership list to list of sets
        N=len(membership)
        CC.sort(key=len) # sort from smaller to bigger
        CC.pop()   # extract largest component from the end of the list
        s = 4/N**2*_compute_suceptibility(CC) # Compute susceptibility
        
        return(s)
    
    def _dist_FET(i,j):
        '''
        i,j: arrays [ vectors (entities) of features  ]  
    
        Returns the p value of a Fisher Exact Test between the features
        of two entities i,j.
        '''
        N_F = len(i) # number of total features (columns)
        n_i = np.dot(i,i) # number of features defining i 
        n_j = np.dot(j,j) # number of features defining j
        n_ij = np.dot(i,j) # number of features common to i and j
    
        contingecy = [[n_ij, n_i - n_ij],             # contingency table
                      [n_j - n_ij, N_F + n_ij - n_i - n_j]]
            
        return fisher_exact(contingecy,alternative='greater')[1] #pvalue


    Z = linkage(A, metric= _dist_FET) # Performs hierarchical clustering on the matrix A using FET distance
    
    
        
    if indexes==True:

    	# We perform the cut of the dendogram at each branch and compute the susceptibility ot the clustering solution.
    	# The metric selected in the parameter 'threshold' choose the best dendrogram cut (by maximizing the selected CVI)

        suceptibility_list=[]
        
        thesholds = [0.999999*x for x in list(Z[:, 2])] # Thresholds to cut are inmediately below dendrogram nodes Z[:, 2]
        for t in thesholds:
            cut = fcluster(Z, t=t, criterion='distance')
            s=_normalizedSusceptibility(cut)
            suceptibility_list.append(s)
            
        CVIs=[]
        CVIs.append(suceptibility_list)
        
        if threshold.isnumeric():
            my_threshold = threshold
        else:
            my_threshold = thesholds[np.where(np.array(suceptibility_list) == max(suceptibility_list))[0][0]] 
        
                
        
        if plot==True:

            fig2 = plt.figure(figsize=(7,3))
            
            plt.plot(thesholds, CVIs[0], label=None,marker='o', markersize=2, linewidth=0.5)
            fig2.subplots_adjust(left=0.1,bottom=0.23,right=0.97, top=0.95)
            #plt.legend(bbox_to_anchor=(0.35, 0.25), loc=1, borderaxespad=0.)
            plt.ylabel('normalized susceptibility')
            plt.xlabel('p-value')
            plt.axvline(x=my_threshold, c='k', ls='-.', lw=0.5,label='p-value = {:0.1e}'.format(my_threshold)+'; susceptibility = {0:.4f}'.format(max(suceptibility_list)))
            plt.legend() 
            plt.xscale('log')
            #ax = plt.axes()
            #ax.xaxis.set_ticks(thesholds)
            #ax.set_xticklabels(['{:0.1e}'.format(t) for t in thesholds], fontsize=xFontSize, rotation=90)

            plt.show()
            
            
            
    print('Best susceptibility cut at  p-value %.2e' % thesholds[np.where(np.array(suceptibility_list) == max(suceptibility_list))[0][0]])
    print(max(suceptibility_list))            
    
    cutree = fcluster(Z, t=my_threshold, criterion='distance') ##Cluster membership of categories under the desired threshold
    
    
    if plot==True:
        hierarchy.set_link_color_palette(['r', 'k', 'c', 'm', 'y', 'g', 'b'])
        fig = plt.figure(figsize=(7,3))
        #plt.title('Hierarchical Clustering Dendrogram')
        plt.xlabel('entities', fontsize=10)
        plt.yscale('log')
        plt.ylabel('p-value')
        dendrogram(
                Z,
                labels=my_labels,
                color_threshold = my_threshold,
                distance_sort='ascending',
                leaf_rotation=90.,  # rotates the x axis labels
                leaf_font_size=xFontSize,  # font size for the x axis labels
                above_threshold_color="grey",
                )
        plt.gca().invert_yaxis()
        plt.ylim(ymin=10**(round(np.log10(min(Z[:,2])))-1),ymax=1)
        #plt.ylim(ymin=1e-300,ymax=1)
        plt.tight_layout()
        ax = plt.subplot(111)
        
        eje_x=[int(ticklabel.get_text()) for ticklabel in ax.get_xticklabels()]
        ground_truth=list(gt.values())
        
        NUM_COLORS = len(list(np.unique(ground_truth)))
        cm = plt.get_cmap('brg')
        cNorm  = colors.Normalize(vmin=0, vmax=NUM_COLORS-1)
        scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
        mis_colores =[scalarMap.to_rgba(i) for i in range(NUM_COLORS)]
        partidos=list(np.unique(ground_truth))
        coloreando = dict(zip(partidos, mis_colores))

        for xtick, color in zip(ax.get_xticklabels(), [coloreando.get(gt.get(str(i))) for i in eje_x]):
            xtick.set_color(color)
        
        #ax.set_xticklabels([item.get_text() for item in ax.get_xticklabels()],color=['blue' if i==2 else 'red' if i==1 else 'black' for i in gt[0].values.tolist()])
        
        #plt.savefig('dendogram_FET.pdf',dpi=900)
        plt.axhline(y=my_threshold, c='k', ls='-.', lw=0.5)
        plt.show()
        
    if plot==True and indexes==True:
        return list(cutree), fig, suceptibility_list, fig2
    else:
        if plot==False and indexes==True:
            return list(cutree), suceptibility_list, thesholds
        else:
            return list(cutree)
    