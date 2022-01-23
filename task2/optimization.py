import oracles
import time
from scipy.special import expit
import numpy as np


class GDClassifier:
    def __init__(
        self, loss_function, step_alpha=1, step_beta=0,
        tolerance=1e-5, max_iter=1000, **kwargs
    ):
        self.loss_function = loss_function
        if self.loss_function == 'binary_logistic':
            self.loss_function = oracles.BinaryLogistic(**kwargs)
        self.step_alpha = step_alpha
        self.step_beta = step_beta
        self.tolerance = tolerance
        self.max_iter = max_iter

    def fit(self, X, y, w_0=None, trace=False, X_val=None, y_val=None):
        if trace is True:
            self.history = {}
            self.history['time'] = []
            self.history['func'] = []
            if X_val is not None and y_val is not None:
                self.history['accuracy'] = []
        if w_0 is None:
            w_k = np.zeros(X.shape[1])
        else:
            w_k = w_0
        self.w = w_k
        f_k = self.loss_function.func(X, y, w_k)
        if trace is True:
            self.history['func'].append(f_k)
            self.history['time'].append(0)
            if X_val is not None and y_val is not None:
                accuracy = (np.where(X_val.dot(self.w) > 0, 1, -1) == y_val).mean()
                self.history['accuracy'].append(accuracy)
        k = 0
        while True:
            if k > self.max_iter:
                break
            start = time.time()
            k += 1
            etha = self.step_alpha / k ** self.step_beta
            w_k1 = w_k - etha * self.loss_function.grad(X, y, w_k)
            f_k1 = self.loss_function.func(X, y, w_k1)
            end = time.time() - start
            if trace is True:
                self.history['time'].append(end)
                self.history['func'].append(f_k1)
                if X_val is not None and y_val is not None:
                    accuracy = (np.where(X_val.dot(w_k1) > 0, 1, -1) == y_val).mean()
                    self.history['accuracy'].append(accuracy)
            if np.absolute(f_k1 - f_k) < self.tolerance:
                break
            w_k = w_k1
            f_k = f_k1
        self.w = w_k
        if trace is True:
            return self.history

    def predict(self, X):
        return np.where(X.dot(self.w) > 0, 1, -1)

    def predict_proba(self, X):
        pos_class = expit(X.dot(self.w))
        neg_class = 1 - pos_class
        return np.concatenate((neg_class, pos_class), axis=1)

    def get_objective(self, X, y):
        return self.loss_function.func(X, y, self.w)

    def get_gradient(self, X, y):
        return self.loss_function.grad(X, y, self.w)

    def get_weights(self):
        return self.w



class BatchGenerator:
    def __init__(self, size, batch_size, shuffle=False):
        self.size = size
        self.batch_size = batch_size
        self.shuffle = shuffle

    def batch_idx(self):
        idx = np.arange(self.size)
        if self.shuffle is True:
            idx = np.random.permutation(idx)
        i = 0
        while i < self.size:
            yield idx[i:i + self.batch_size]
            i += self.batch_size

    def __iter__(self):
        idx = self.batch_idx()
        for ind in idx:
            yield [i for i in ind]



class SGDClassifier(GDClassifier):
    def __init__(
        self, loss_function, batch_size, step_alpha=1, step_beta=0,
        tolerance=1e-5, max_iter=1000, random_seed=153, **kwargs
    ):
        self.loss_function = loss_function
        if self.loss_function == 'binary_logistic':
            self.loss_function = oracles.BinaryLogistic(**kwargs)
        self.batch_size = batch_size
        self.step_alpha = step_alpha
        self.step_beta = step_beta
        self.tolerance = tolerance
        self.max_iter = max_iter
        self.random_seed = random_seed

    def fit(self, X, y, w_0=None, trace=False, log_freq=1.0, X_val=None, y_val=None):
        np.random.seed(self.random_seed)
        if trace is True:
            self.history = {}
            self.history['epoch_num'] = []
            self.history['time'] = []
            self.history['func'] = []
            self.history['weights_diff'] = []
            self.history['iteration'] = []
            if X_val is not None and y_val is not None:
                self.history['accuracy'] = []
        if w_0 is None:
            w_k = np.zeros(X.shape[1])
        else:
            w_k = w_0
        self.w = w_k
        epoch_num = 0
        epoch_num1 = 0
        k = 0
        f_k = self.loss_function.func(X, y, self.w)
        if trace is True:
            self.history['time'].append(0)
            self.history['epoch_num'].append(0)
            self.history['func'].append(f_k)
            if X_val is not None and y_val is not None:
                accuracy = (np.where(X_val.dot(self.w) > 0, 1, -1) == y_val).mean()
                self.history['accuracy'].append(accuracy)
            self.history['iteration'].append(0)
        flag = True
        while flag:
            for b in np.array_split(np.random.permutation(X.shape[0]), X.shape[0] // self.batch_size):
                if k > self.max_iter:
                    flag = False
                    break
                k += 1
                start = time.time()
                etha = self.step_alpha / k ** self.step_beta
                w_k1 = w_k - etha * self.loss_function.grad(X[b], y[b], w_k)
                f_k1 = self.loss_function.func(X, y, w_k1)
                end = time.time() - start
                epoch_num1 += self.batch_size / X.shape[0]
                if trace is True and epoch_num1 - epoch_num > log_freq:
                    self.history['epoch_num'].append(epoch_num1)
                    self.history['time'].append(end)
                    self.history['func'].append(f_k1)
                    diff = np.linalg.norm(w_k1 - w_k) ** 2
                    self.history['weights_diff'].append(diff)
                    if X_val is not None and y_val is not None:
                        accuracy = (np.where(X_val.dot(w_k1) > 0, 1, -1) == y_val).mean()
                        self.history['accuracy'].append(accuracy)
                    self.history['iteration'].append(k)
                    epoch_num = epoch_num1
                    if np.absolute(f_k1 - self.history['func'][-2]) < self.tolerance:
                        flag = False
                        break

                w_k = w_k1
                f_k = f_k1
        self.w = w_k
        if trace is True:
            return self.history
