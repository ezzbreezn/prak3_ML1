import numpy as np


def calc_expectations(h, w, X, Q):
    H = X.shape[0]
    W = X.shape[1]
    #res = np.zeros(X.shape)
    #for i in range(H):
    #    for j in range(W):
    #        start_row = max(0, i - h + 1)
    #        start_col = max(0, j - w + 1)
    #        res[i][j] = Q[start_row:i + 1, start_col:j + 1].sum()
    #return res * X
    M1 = np.roll(Q, w, axis=1) * -1
    M1[:, :w] = 0
    Q = Q + M1
    for i in range(H):
        for j in range(1, W):
            Q[i][j] += Q[i][j - 1]
    M2 = np.roll(Q, h, axis=0) * -1
    M2[:h, :] = 0
    Q = Q + M2
    for j in range(W):
        for i in range(1, H):
            Q[i][j] += Q[i - 1][j]
    return X * Q

X = np.array([[1,1,1,1],[2,2,2,2],[3,3,3,3],[4,4,4,4]])
Q = np.array([[0.2,0,0.3,0.1],[0.1,0,0.2,0],[0.05,0,0,0],[0,0,0,0.05]])
print(calc_expectations(2, 2, X, Q))
