import copy


class CooSparseMatrix:
    def __init__(self, ijx_list, shape):
        if shape[0] < 0 or shape[1] < 0:
            raise TypeError("incorrect shape")
        elif type(shape) is not tuple:
            raise TypeError("incorrect shape")
        elif type(shape[0]) is not int or type(shape[1]) is not int:
            raise TypeError("incorrect shape")
        self.dok = {}
        self.__shape = shape
        for t in ijx_list:
            if t[0] >= shape[0] or t[1] >= shape[1] or t[0] < 0 or t[1] < 0:
                raise TypeError("incorrect position")
            elif type(t[0]) is not int or type(t[1]) is not int:
                raise TypeError("incorrect position")
            if t[0] in self.dok.keys() and t[1] in self.dok[t[0]].keys():
                raise TypeError("duplicate elements")
            if t[0] not in self.dok.keys():
                self.dok[t[0]] = {}
            if t[2] != 0:
                self.dok[t[0]][t[1]] = t[2]

    def __getitem__(self, key):
        if type(key) is int:
            if key < 0 or key >= self.shape[0]:
                raise TypeError("incorrect position")
            new_shape = (1, self.shape[1])
            res = CooSparseMatrix([], new_shape)
            if key in self.dok.keys():
                res.dok[0] = self.dok[key]
            return res
        elif type(key) is tuple:
            i = key[0]
            j = key[1]
            if type(i) is not int or type(j) is not int:
                raise TypeError("incorrect posotion")
            if i < 0 or i >= self.shape[0] or j < 0 or j >= self.shape[1]:
                raise TypeError("incorrect position")
            if not (i in self.dok.keys() and j in self.dok[i].keys()):
                return 0
            else:
                return self.dok[i][j]
        else:
            raise TypeError("incorrect position")

    def __setitem__(self, idx, value):
        if value != 0:
            if type(idx[0]) is not int or type(idx[1]) is not int:
                raise TypeError("incorrect position")
            elif idx[0] < 0 or idx[0] >= self.shape[0]:
                raise TypeError("incorrect position")
            elif idx[1] < 0 or idx[1] >= self.shape[1]:
                raise TypeError("incorrect position")
            if idx[0] not in self.dok.keys():
                self.dok[idx[0]] = {}
            self.dok[idx[0]][idx[1]] = value
        else:
            if idx[0] in self.dok.keys() and idx[1] in self.dok[idx[0]].keys():
                del self.dok[idx[0]][idx[1]]

    def __add__(self, s):
        if not isinstance(s, CooSparseMatrix):
            raise TypeError("incorrect type")
        if self.shape != s.shape:
            raise TypeError("incorrect matrix size")
        r = CooSparseMatrix([], self.shape)
        r.dok = copy.deepcopy(self.dok)
        for k in s.dok.keys():
            if k not in r.dok.keys():
                r.dok[k] = copy.deepcopy(s.dok[k])
            else:
                r.dok[k] = {i: r.dok[k].get(i, 0) + s.dok[k].get(i, 0)
                            for i in set(r.dok[k]) | set(s.dok[k])
                            if r.dok[k].get(i, 0) + s.dok[k].get(i, 0) != 0}
        return r

    def __sub__(self, s):
        if not isinstance(s, CooSparseMatrix):
            raise TypeError("incorrect type")
        if self.shape != s.shape:
            raise TypeError("incorrect matrix size")
        r = CooSparseMatrix([], self.shape)
        r.dok = copy.deepcopy(self.dok)
        for k in s.dok.keys():
            if k not in r.dok.keys():
                r.dok[k] = copy.deepcopy(s.dok[k])
                for i in r.dok[k].keys():
                    r.dok[k][i] *= -1
            else:
                r.dok[k] = {i: r.dok[k].get(i, 0) - s.dok[k].get(i, 0)
                            for i in set(r.dok[k]) | set(s.dok[k])
                            if r.dok[k].get(i, 0) - s.dok[k].get(i, 0) != 0}
        return r

    def __mul__(self, s):
        if type(s) is not float and type(s) is not int:
            raise TypeError("incorrect value")
        r = CooSparseMatrix([], self.shape)
        if s == 0:
            r.dok = {}
            return r
        r.dok = copy.deepcopy(self.dok)
        for k in r.dok.keys():
            for t in r.dok[k].keys():
                r.dok[k][t] *= s
        return r

    def __rmul__(self, s):
        if type(s) is not float and type(s) is not int:
            raise TypeError("incorrect value")
        r = CooSparseMatrix([], self.shape)
        if s == 0:
            r.dok = {}
            return r
        r.dok = copy.deepcopy(self.dok)
        for k in r.dok.keys():
            for t in r.dok[k].keys():
                r.dok[k][t] *= s
        return r

    def set_shape(self, shape):
        if type(shape) is not tuple or shape[0] <= 0 or shape[1] <= 0:
            raise TypeError("incorrect shape")
        elif type(shape[0]) is not int or type(shape[1]) is not int:
            raise TypeError("incorrect shape")
        elif self.__shape[0] * self.__shape[1] != shape[0] * shape[1]:
            raise TypeError("incorrect shape")
        new_dok = {}
        for k1 in self.dok.keys():
            for k2 in self.dok[k1].keys():
                num = k1 * self.__shape[1] + k2
                row = num // shape[1]
                col = num % shape[1]
                if row not in new_dok.keys():
                    new_dok[row] = {}
                new_dok[row][col] = self.dok[k1][k2]
        self.__shape = shape
        self.dok = new_dok

    def get_shape(self):
        return self.__shape

    shape = property(get_shape, set_shape)

    def get_t(self):
        res = CooSparseMatrix([], (self.shape[1], self.shape[0]))
        res.dok = {}
        for k1 in self.dok.keys():
            for k2 in self.dok[k1].keys():
                if k2 not in res.dok.keys():
                    res.dok[k2] = {}
                res.dok[k2][k1] = self.dok[k1][k2]
        return res

    T = property(get_t)
