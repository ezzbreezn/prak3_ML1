import numpy as np
import nearest_neighbors


def kfold(n, n_folds):
    source_idx = np.arange(n)
    res = []
    start = 0
    for i in range(n_folds):
        size = int(np.ceil(n / n_folds))
        validation = source_idx[i * size:(i + 1) * size]
        train_idx = np.concatenate(
            (np.arange(0, i * size), np.arange((i + 1) * size, n))
        )
        train = source_idx[train_idx]
        res.append((train, validation))
    return res


def mode(X):
    vals, counts = np.unique(X, return_counts=True)
    idx = np.argmax(counts)
    return vals[idx]


def knn_cross_val_score(X, y, k_list, score, cv, **kwargs):
    ans = {}
    if type(cv) is int:
        idx = kfold(X.shape[0], cv)
    elif cv is None:
        idx = kfold(X.shape[0], 3)
    else:
        idx = cv
    length = len(idx)
    len_k = len(k_list)
    for i in range(length):
        clf = nearest_neighbors.KNNClassifier(k_list[-1], **kwargs)
        clf.fit(X[idx[i][0]], y[idx[i][0]])
        if clf.weights is True:
            dists, index = clf.find_kneighbors(X[idx[i][1]], True)
            ans_weights = 1 / (dists + 10 ** (-5))
        else:
            index = clf.find_kneighbors(X[idx[i][1]], False)
        index = index.astype('int64')
        labels = y[idx[i][0]][index]
        for j in range(len_k):
            if clf.weights is True:
                res = np.zeros(index.shape[0])
                for t in range(index.shape[0]):
                    votes = {}
                    for s in range(k_list[j]):
                        if labels[t, s] not in votes:
                            votes[labels[t, s]] = 0
                        votes[labels[t, s]] += ans_weights[t, s]
                    res[t] = max(votes, key=votes.get)
                res = res.astype('int64')
            else:
                res = np.apply_along_axis(mode, axis=1, arr=labels[:, :k_list[j]])
            accuracy = (y[idx[i][1]] == res).sum() / res.shape[0]
            if k_list[j] not in ans:
                ans[k_list[j]] = np.zeros(length)
            ans[k_list[j]][i] = accuracy
    return ans
