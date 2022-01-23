def get_nonzero_diag_product(X):
    res = X.diagonal()[X.diagonal() != 0]
    if res.size == 0:
        return None
    else:
        return res.prod()
