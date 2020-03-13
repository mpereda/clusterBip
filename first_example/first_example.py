from hierarchical_bipartite import hierarchical_bipartite
   
# import some data to play with

# Let's analyze the shopping list of 100 people choosing among 20 products to buy
datos = pd.read_csv('data/shopping_list.csv', dtype='category', sep=',')  
datos = datos.set_index("Labels") #Label column to row names

#Let's explore the data
print(datos.head(3))
#We want to see which products are more likely to be purchased together

#Ensure your matrix has the entities you want to cluster as rows, and the features as columns
datos=datos.T
#Get the entities labels
entities_labels=list(datos.index) 

results = hierarchical_bipartite(datos,entities_labels,plot=True,indexes=True, xFontSize=8)

# In the dendrogram, you'll see in colors different groups (clusters) of products that are more likely to be purchased together
results[1]

#You can obtain an ordered list of the cluster membership (for each entitie, the list shows the ID of the cluster it belongs)
results[0]

# The normalized susceptibility plot as a function of the p-values of the dendrogram can be shown as:
results[3]
