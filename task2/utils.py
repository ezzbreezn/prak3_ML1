import numpy as np


def grad_finite_diff(function, w, eps=1e-8):
    result = np.apply_along_axis(function, 1, w + np.diag(np.full(len(w), eps)))
    return (result - function(w)) / eps
