import numpy as np
from scipy.special import expit


class BaseSmoothOracle:
    def func(self, w):
        raise NotImplementedError('Func oracle is not implemented.')

    def grad(self, w):
        raise NotImplementedError('Grad oracle is not implemented.')


class BinaryLogistic(BaseSmoothOracle):
    def __init__(self, l2_coef):
        self.l2_coef = l2_coef

    def func(self, X, y, w):
        loss = np.sum(np.logaddexp(0, -y * (X.dot(w)))) / X.shape[0]
        return loss + np.linalg.norm(w) ** 2 * self.l2_coef / 2

    def grad(self, X, y, w):
        res = -X.T.dot(y * expit(-y * (X.dot(w)))) / X.shape[0]
        return res + self.l2_coef * w
