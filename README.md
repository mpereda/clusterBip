

clusterBip written by Ignacio Tamarit, María Pereda, and Jose A. Cuesta

# LICENSE
This library is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.

# clusterBip
clusterBip is a Python library to cluster bipartite data sets based on the statistical significance of coincidences.

# Quickstart
**install:**

    You do not need to install anything.

**example of usage:**

Firstly, load the function:

    from hierarchical_bipartite import hierarchical_bipartite
       
Then, import some data to play with. Let's analyze the shopping list of 100 people choosing among 20 products to buy. We want to study which products are more likely to be purchased together

   

    datos = pd.read_csv('data/shopping_list.csv', dtype='category', sep=',')  
    datos = datos.set_index("Labels") #Label column to row names

Let's explore the data
	

    print(datos.head(3))

Ensure your matrix has the entities you want to cluster as rows, and the features as columns:

    datos=datos.T
    #Get the entities labels
    entities_labels=list(datos.index) 

Call the function and wait for the magic:
	

    results = hierarchical_bipartite(datos,entities_labels,plot=True,indexes=True, xFontSize=8)

In the dendrogram, you'll see in colors different groups (clusters) of products that are more likely to be purchased together
	

    results[1]

You can obtain an ordered list of the cluster membership (for each entitie, the list shows the ID of the cluster it belongs)
	

    results[0]

The normalized susceptibility plot as a function of the p-values of the dendrogram can be shown as:
    	

    results[3]
