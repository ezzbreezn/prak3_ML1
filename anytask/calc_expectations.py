import numpy as np


def calc_expectations(h, w, X, Q):
    M1 = np.roll(Q, w, axis=1) * -1
    M1[:, :w] = 0
    Q = Q + M1
    Q = np.cumsum(Q, axis=1)
    M2 = np.roll(Q, h, axis=0) * -1
    M2[:h, :] = 0
    Q = Q + M2
    Q = np.cumsum(Q, axis=0)
    return X * Q
