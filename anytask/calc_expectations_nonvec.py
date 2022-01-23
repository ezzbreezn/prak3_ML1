import numpy as np


def calc_expectations(h, w, X, Q):
    H = X.shape[0]
    W = X.shape[1]
    S = [([0] * W) for i in range(H)]
    for i in range(H):
        for j in range(W):
            start_row = max(0, i - h + 1)
            start_col = max(0, j - w + 1)
            for k in range(start_row, i + 1):
                for t in range(start_col, j + 1):
                    S[i][j] += Q[k][t]
            S[i][j] *= X[i][j]
    return S

X = np.array([[1,1,1,1],[2,2,2,2],[3,3,3,3],[4,4,4,4]])
Q = np.array([[0.2,0,0.3,0.1],[0.1,0,0.2,0],[0.05,0,0,0],[0,0,0,0.05]])
print(calc_expectations(2, 2, X, Q))
