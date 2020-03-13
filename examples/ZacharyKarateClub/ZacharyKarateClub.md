# the Zaccary karate club network

Let's analize a well known bipartite network: the Zaccary karate club: *Zachary, W. W. (1977) An information flow model for conflict and fission in smallgroups.J. Anthropol. Res.,33(4), 452–473*

We are goint to use the function *hierarchical_bipartite_color* to color the labels of the entities in the dendrogram:

    from hierarchical_bipartite import hierarchical_bipartite
       
We load both the bipartite network and its ground truth:

    datos = pd.read_csv('zachary_A_diagonal.csv', dtype='category', sep=';', header=None)  # read file 
    labels1=[str(i+1) for i in range(datos.shape[0])]

    clusters = pd.read_csv('zachary_gt.txt', dtype='int', sep=' ', delimiter='\t', header=None) #red original Zackary
    # We save the ground truth in a dictionary
    gt = dict(zip(labels1, clusters[0])) 

Then we just call the function:

    results = hierarchical_bipartite_color(datos,labels1,gt, plot=True,indexes=True, xFontSize=8)


In the dendrogram, you'll see the colors of the two groups of people, and the labels are now colored according to the ground truth:
	
    results[1]
![ZKC_dendro](ZKC_dendro.png?raw=true "Title")
