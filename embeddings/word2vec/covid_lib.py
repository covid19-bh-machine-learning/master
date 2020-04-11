import pandas as pd
from Bio import SeqIO
from Bio.Alphabet import generic_protein
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline
from sklearn.manifold import TSNE
from scipy.cluster.hierarchy import fcluster
from sklearn import preprocessing


import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def reduce_dimensions(model, ordered_indexes, corpus, df, label="Species",
                     perplexity=30, n_iter = 500):
    num_dimensions = 2  # final num dimensions (2D, 3D, etc)
    
    vectors = [] # positions in vector space
    labels = [] # keep track of words to label our data again later

    for i, sentence in zip(ordered_indexes, corpus):

        vectors.append(np.mean([model.wv[word] for word in sentence], axis=0))
        labels.append(df.iloc[i][label])
        
    # convert both lists into numpy vectors for reduction
    vectors = np.asarray(vectors)
    labels = np.asarray(labels)

    # reduce using t-SNE
    vectors = np.asarray(vectors)
    tsne = TSNE(n_components=num_dimensions, random_state=0, perplexity=perplexity, n_iter=n_iter)
    vectors = tsne.fit_transform(vectors)

    x_vals = [v[0] for v in vectors]
    y_vals = [v[1] for v in vectors]
    return x_vals, y_vals, labels

def plot_with_matplotlib(x_vals, y_vals, labels, color_labels):
    import matplotlib.pyplot as plt
    import random

    random.seed(0)

    le = preprocessing.LabelEncoder()
    le.fit(color_labels)
    cmappable_labels = le.transform(color_labels)
    
    fig, ax = plt.subplots(1, figsize=(10, 10))
    unique = np.unique(color_labels)
    colors = [plt.cm.rainbow(i/float(len(unique)-1)) for i in range(len(unique))]
    for i, u in enumerate(unique):
        xi = [x_vals[j] for j  in range(len(x_vals)) if color_labels[j] == u]
        yi = [y_vals[j] for j  in range(len(x_vals)) if color_labels[j] == u]
        
        edgecolor =None
        if u == "Homo":
            edgecolor ='k'
        elif u == "Felis":
            edgecolor ='r'
        plt.scatter(xi, yi, c=(colors[i],), label=str(u), edgecolor=edgecolor)
        
    plt.legend(bbox_to_anchor=(1.05, 1.0, 0.3, 0.2), loc='upper left')
    
    selected_indices = [i for i,s in enumerate(labels) if "coronavirus 2" in s]
    for i in selected_indices:
        plt.annotate('°', (x_vals[i], y_vals[i]))
    
    return fig,ax

def get_clusters(linkage, numclust, labels, norm=True):
    """extracts numclust clusters from the linkage matrix
    if norm: True returns the fraction with respect to the total number of points with the same label"""
    d = {}
    totals = {}
    fl = fcluster(linkage,numclust,criterion='maxclust')
    labs = np.array(labels)
    
    unique_elements, counts_elements = np.unique(labs, return_counts=True)
    for host, counts in zip(unique_elements, counts_elements):
        totals[host] = counts
    
    for i in np.arange(1, numclust+1):
        d[i] = {}
        uniq, cnt = np.unique(labs[fl == i], return_counts=True)
        for host, counts in zip(uniq, cnt):
            if totals[host] > 5:
                d[i][host] = counts/totals[host]
    return d, labs

def cons_matrix(labels):
    C=np.zeros([labels.shape[1],labels.shape[1]], np.int32)
    for label in labels:
        for i, val1 in enumerate(label):
            for j, val2 in enumerate(label):
                #filling C_ij
                
                if val1 == val2 :
                    C[i,j] += 1 
                    
                ##and with a list comprehension?
                
    
    return pd.DataFrame(C)

def getNewick(node, newick, parentdist, leaf_names):
    if node.is_leaf():
        return "%s:%.2f%s" % (leaf_names[node.id], parentdist - node.dist, newick)
    else:
        if len(newick) > 0:
            newick = "):%.2f%s" % (parentdist - node.dist, newick)
        else:
            newick = ");"
        newick = getNewick(node.get_left(), newick, node.dist, leaf_names)
        newick = getNewick(node.get_right(), ",%s" % (newick), node.dist, leaf_names)
        newick = "(%s" % (newick)
        return newick
