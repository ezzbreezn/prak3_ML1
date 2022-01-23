import numpy as np
import distances


class KNNClassifier:
    def __init__(self, k, strategy, metric, weights, test_block_size):
        self.k = k
        self.strategy = strategy
        if strategy not in ['my_own', 'brute', 'kd_tree', 'ball_tree']:
            raise ValueError('incorrect strategy')
        self.metric = metric
        if metric not in ['euclidean', 'cosine']:
            raise ValueError('incorrect metric')
        self.weights = weights
        self.test_block_size = test_block_size
        if strategy != 'my_own':
            from sklearn.neighbors import NearestNeighbors
            self.algorithm = NearestNeighbors(
                                    n_neighbors=k,
                                    algorithm=strategy,
                                    metric=metric)

    def fit(self, X, y):
        self.train_data = X
        self.train_answers = y
        if self.strategy != 'my_own':
            self.algorithm.fit(X)

    def find_kneighbors(self, X, return_distance):
        start = 0
        stop = self.test_block_size
        if return_distance is True:
            dists = np.zeros((X.shape[0], self.k))
        idx = np.zeros((X.shape[0], self.k))
        while start < X.shape[0]:
            if self.strategy == 'my_own':
                if self.metric == 'euclidean':
                    temp_dist = distances.euclidean_distance(
                        X[start:stop, :],
                        self.train_data
                    )
                elif self.metric == 'cosine':
                    temp_dist = distances.cosine_distance(
                        X[start:stop, :],
                        self.train_data
                    )
                sorted_idx = np.argsort(temp_dist, axis=1)[:, :self.k]
                if return_distance is True:
                    row_index = np.arange(temp_dist.shape[0])[:, np.newaxis]
                    dists[start:stop, :] = temp_dist[row_index, sorted_idx]
                idx[start:stop, :] = sorted_idx

            else:
                res = self.algorithm.kneighbors(
                    X[start:stop, :],
                    return_distance=return_distance
                )
                if return_distance is True:
                    dists[start:stop] = res[0]
                    idx[start:stop] = res[1]
                else:
                    idx[start:stop] = res
            start += self.test_block_size
            stop += self.test_block_size
        if return_distance is True:
            return (dists, idx)
        else:
            return idx

    def mode(self, X):
        vals, counts = np.unique(X, return_counts=True)
        idx = np.argmax(counts)
        return vals[idx]

    def predict(self, X):
        if self.weights is False:
            idx = self.find_kneighbors(X, False)
            answers = self.train_answers[idx.astype('int64')]
            return np.apply_along_axis(self.mode, axis=1, arr=answers)
        else:
            dists, idx = self.find_kneighbors(X, True)
            answers = self.train_answers[idx.astype('int64')]
            ans_weights = 1 / (dists + 10 ** (-5))
            res = np.zeros(X.shape[0])
            for i in range(answers.shape[0]):
                votes = {}
                for j in range(answers.shape[1]):
                    if answers[i, j] not in votes:
                        votes[answers[i, j]] = 0
                    votes[answers[i, j]] += ans_weights[i, j]
                res[i] = max(votes, key=votes.get)
            return res.astype('int64')
