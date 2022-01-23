import numpy as np


def replace_nan_to_means(X):
    Y = np.copy(X)
    idx = np.where(np.isnan(X))
    Y[idx] = np.take(np.nanmean(X, axis=0), idx[1])
    return Y
