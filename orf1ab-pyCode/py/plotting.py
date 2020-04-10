
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE


def _plot_scatter(color_by, x_tsne):
    # sns settings
    sns.set(rc={'figure.figsize':(15,15)})
    # colors
    palette = sns.color_palette("bright", len(set(color_by)))
    # plot
    sns.scatterplot(x_tsne[:,0], x_tsne[:,1], hue=color_by, legend='full', palette=palette)
    plt.title("t-SNE K-means clusters")
    # plt.savefig("plots/plot.png")
    plt.show()

def plot_tsne(xtrain_ctv, ytrain, perplexity):
    '''
    ytrain: train labels
    xtrain_ctv: embedding matrix - train data
    perplexity: t-sne variable
    plots a t-SNE scatterplot
    '''
    tsne = TSNE(verbose=1, perplexity=perplexity)
    x_tsne = tsne.fit_transform(xtrain_ctv)
    _plot_scatter(ytrain, x_tsne)
