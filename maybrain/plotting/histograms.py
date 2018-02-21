import matplotlib.pyplot as plt
import numpy as np
import networkx as nx


def show():
    """
    Show all the figures generated by matplotlib
    This function is equivalent to :func:`matplotlib.pyplot.show`.
    """
    plt.show()


def plot_weight_distribution(brain, output_file=None, **kwargs):
    """ 
    It uses matplotlib to plot a histogram of the weights of the edges.
    Requires that the brain was thresholded before and ignores NaNs for plotting

    brain: an instance of the Brain class or nx.Graph
    output_file: if you want to create a file. It then calls fig.savefig(output_file) from matplotlib
    **kwargs: keyword arguments if you need to pass them to matplotlib's hist()

    return: if output_file is None, this returns (fig, ax) from the figure created
    """
    fig, ax = plt.subplots()

    if type(brain) == nx.Graph:
        arr = np.copy(nx.to_numpy_matrix(brain, nonedge=np.nan))
    else:
        arr = np.copy(nx.to_numpy_matrix(brain.G, nonedge=np.nan))

    upper_values = np.triu_indices(np.shape(arr)[0], k=1)
    weights = np.array(arr[upper_values])

    # If directed, also add the lower down part of the adjacency matrix
    if type(brain) != nx.Graph and brain.directed:
        below_values = np.tril_indices(np.shape(arr)[0], k=-1)
        weights.extend(np.array(below_values))

    # Removing NaNs for correct plotting
    weights = weights[~np.isnan(weights)]

    # the histogram of the data
    ax.hist(weights, **kwargs)
    ax.set_title('Weights')

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()

    # If outputfile is defined, fig is correctly closed, otherwise returned so others can add more information to it
    if output_file is not None:
        fig.savefig(output_file)
        plt.close(fig)
    else:
        return fig, ax

