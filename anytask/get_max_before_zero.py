import numpy as np


def get_max_before_zero(x):
    idx = np.argwhere(x == 0)
    if idx.size == 0:
        return None
    idx += 1
    if idx[-1] >= x.shape[0]:
        idx = idx[:-1]
        if idx.size == 0:
            return None
    return np.max(x[idx])
