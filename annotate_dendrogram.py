import numpy as np
from matplotlib import pyplot as plt


def get_leaves_from_linkage(Z, cluster, labels):
    """Get the leaves of a cluster in the linkage matrix.

    Parameters
    ----------
    Z : ndarray, shape (n_clusters, n_levels)
        The linkage matrix as returned by the linkage function.
    cluster : int
        Index of the cluster to obtain the leaves for.
    labels : list
        The labels for all the leaves in the dengrogram.

    Returns
    -------
    leaves : list
        The labels corresponding to the leaves of the cluster.

    Example
    -------
    >>> import numpy as np
    ... from scipy.cluster.hierarchy import linkage
    ... labels = ['a', 'b', 'c']
    ... dist = [1, 2, 3]
    ... Z = linkage(dist)
    ... get_leaves_from_linkage(Z, 3, labels)
    ['a', 'b']

    See also
    --------
    get_leaves_from_dendrogram
    """
    n = len(labels)
    if n == 0:
        return []

    leaves = []
    if cluster < n:
        leaves.append(labels[cluster])
    else:
        leaves += get_leaves_from_linkage(Z, int(Z[cluster - n][0]), labels)
        leaves += get_leaves_from_linkage(Z, int(Z[cluster - n][1]), labels)

    return leaves


def apply_along_nodes(Z, labels, func, args=[]):
    """Apply a function along the nodes of a dendrogram.

    Parameters
    ----------
    Z : ndarray, shape (n_clusters, n_levels)
        The linkage matrix as returned by the linkage function.
    labels : list
        The labels for all the leaves in the dengrogram.
    func : function (left, right, *args)
        The function that will be called for each node in the dendrogram.
        First argument is the leaves on the left side of the node.
        Second argument is the leaves on the left side of the node.
    args : list
        This list will be added as extra arguments when calling `func`.

    Returns
    -------
    results : list
        For each node in the dendrogram, the results returned by `func`.
    """
    results = []
    for node in Z:
        group1 = get_leaves_from_linkage(Z, int(node[0]), labels)
        group2 = get_leaves_from_linkage(Z, int(node[1]), labels)
        if len(group1) > 0 and len(group2) > 0:
            result = func(group1, group2, *args)
            results.append(result)

    return results


def get_leaves_from_dendrogram(dendrogram, cluster, labels):
    """Get the leaves of a cluster in a dendrogram.

    Parameters
    ----------
    dendrogram : dict
        Information about the dendrogram as returned by the `dendrogram`
        function.
    cluster : int
        Index of the cluster to obtain the leaves for.
    labels : list
        The labels for all the leaves in the dengrogram.

    Returns
    -------
    leaves : list
        The labels corresponding to the leaves of the cluster.

    Example
    -------
    >>> import numpy as np
    ... from scipy.cluster.hierarchy import linkage, dendrogram
    ... labels = ['a', 'b', 'c']
    ... dist = [1, 2, 3]
    ... Z = linkage(dist)
    ... d = dendrogram(Z, labels)
    ... get_leaves_from_dendrogram(d, 3, labels)
    ['a', 'b']

    See also
    --------
    get_leaves_from_linkage
    """
    icoord = np.array(dendrogram['icoord'])
    dcoord = np.array(dendrogram['dcoord'])
    leaves = dendrogram['leaves']
    x = icoord[cluster].astype(np.int)
    y = dcoord[cluster].astype(np.int)

    left = []
    if y[0] == 0 and (x[0] - 5) % 10 == 0:
        # Connects to leaf
        ind = leaves[int(x[0] - 5) / 10]
        left.append(labels[ind])
    else:
        # Connects to other cluster
        connecting_cluster = np.argmin(
            np.abs(icoord[:, 1:3].mean(axis=1) - x[0]) +
            np.abs(dcoord[:, 1] - y[0])
        )
        left += get_leaves_from_dendrogram(dendrogram, connecting_cluster,
                                           labels)

    right = []
    if y[3] == 0 and (x[3] - 5) % 10 == 0:
        # Connects to leaf
        ind = dendrogram['leaves'][int(x[3] - 5) / 10]
        right.append(labels[ind])
    else:
        # Connects to other cluster
        connecting_cluster = np.argmin(
            np.abs(icoord[:, 1:3].mean(axis=1) - x[3]) +
            np.abs(dcoord[:, 2] - y[3])
        )
        right += get_leaves_from_dendrogram(dendrogram, connecting_cluster,
                                            labels)

    return left + right


def match_linkage_to_dendrogram(Z, dendrogram, labels):
    """Match the order of the nodes in the linkage matrix and dendrogram.

    Annoyingly, the `dendrogram` function does not return its information about
    the nodes in the same order as they are specified in the linkage matrix.
    This function tries to find, for each node in the linkage matrix, the
    corresponding node in the dendrogram. This may not always succeed, in which
    case a `RuntimeException` is raised.

    Parameters
    ----------
    Z : ndarray, shape (n_clusters, n_levels)
        The linkage matrix as returned by the linkage function.
    dendrogram : dict
        Information about the dendrogram as returned by the `dendrogram`
        function.
    labels : list
        The labels for all the leaves in the dengrogram.

    Returns
    -------
    mapping : list of int
        For each node in the linkage matrix, the index of the corresponding
        node in the dendrogram.
    """

    linkage_leaves = []
    n = len(labels)
    for i in range(len(Z)):
        linkage_leaves.append(set(get_leaves_from_linkage(Z, i + n, labels)))

    mapping = []
    for j in range(len(dendrogram['dcoord'])):
        dendrogram_leaves = get_leaves_from_dendrogram(dendrogram, j, labels)
        dendrogram_leaves = set(dendrogram_leaves)
        for k in range(len(linkage_leaves)):
            if linkage_leaves[k] == dendrogram_leaves:
                mapping.append(k)
                break
        else:
            raise RuntimeError('Could not find a match for node %d (%s)' %
                               (j, dendrogram_leaves))

    return mapping


def annotate_dendrogram(Z, dendrogram, labels, func, args=[], voffset=-5,
                        annotate_args={}):
    """Annotate the nodes of a dendrogram with string labels.

    Parameters
    ----------
    Z : ndarray, shape (n_clusters, n_levels)
        The linkage matrix as returned by the linkage function.
    dendrogram : dict
        Information about the dendrogram as returned by the `dendrogram`
        function.
    labels : list
        The labels for all the leaves in the dengrogram.
    func : function (left, right, *args)
        The function that will be called for each node in the dendrogram.
        First argument is the leaves on the left side of the node.
        Second argument is the leaves on the left side of the node.
        The function should return a text label to annotate the node with.
    args : list
        This list will be added as extra arguments when calling `func`.
    voffset : int
        The vertical offset (in pixels), measured from the center of the node,
        to place the annotation at. Defaults to -5.
    annotate_args : dict
        Any parameters to pass along to matplotlib's `plt.annotate`
        function that is drawing the annotations. By default, the following
        parameters are used:
            ha = 'center',
            va = 'top',
            family = 'verdana',
            fontsize = 10,
            backgroundcolor = (1, 1, 1, 0.6),
    """
    default_annotate_args = dict(
        ha='center',
        va='top',
        family='verdana',
        fontsize=10,
        backgroundcolor=(1, 1, 1, 0.6),
    )
    default_annotate_args.update(annotate_args)

    n_nodes = len(dendrogram['dcoord'])
    dcoord = np.array(dendrogram['dcoord'])
    icoord = np.array(dendrogram['icoord'])
    mapping = match_linkage_to_dendrogram(Z, dendrogram, labels)
    annotations = apply_along_nodes(Z, labels, func, args)

    # Annotate nodes
    for node in range(n_nodes):
        plt.annotate(
            annotations[mapping[node]],
            xy=(icoord[node].mean(), dcoord[node].max()),
            xytext=(0, voffset),
            textcoords='offset points',
            **default_annotate_args
        )
