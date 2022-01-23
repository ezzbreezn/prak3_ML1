import numpy as np


def encode_rle(x):
    if x.size == 0:
        return (None, None)
    else:
        cond = x[1:] != x[:-1]
        idx = np.append(np.where(cond), x.size - 1)
        times = np.diff(np.append(-1, idx))
        return (x[idx], times)
