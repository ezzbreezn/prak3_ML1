import numpy as np


def euclidean_distance(X, Y):
    X_rows = np.sum(X**2, axis=1)[:, np.newaxis]
    Y_rows = np.sum(Y**2, axis=1)
    mixed = -2 * (X @ Y.T)
    return np.sqrt(X_rows + Y_rows + mixed)


def cosine_distance(X, Y):
    norms = np.linalg.norm(X, axis=1)[:, np.newaxis] @ \
            np.linalg.norm(Y, axis=1)[:, np.newaxis].T
    return 1 - (X @ Y.T) / norms
