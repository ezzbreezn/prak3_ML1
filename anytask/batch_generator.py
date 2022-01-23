import numpy as np


class BatchGenerator:
    def __init__(self, list_of_sequences, batch_size, shuffle=False):
        self.sequence = list_of_sequences
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.size = len(list_of_sequences[0])

    def batch_idx(self):
        idx = np.arange(self.size)
        if self.shuffle is True:
            np.random.seed(0)
            idx = np.random.permutation(idx)
        i = 0
        while i < self.size:
            yield idx[i:i + self.batch_size]
            i += self.batch_size

    def __iter__(self):
        idx = self.batch_idx()
        for ind in idx:
            yield [[elem[i] for i in ind] for elem in self.sequence]

X = np.array([[1,0,0,0],[1,1,1,1],[0,1,1,0],[0,1,1,1]])
y = np.array([1,0,1,1])
bg = BatchGenerator([X, y], 2, True)
for elem in bg:
    print(elem)
for elem in bg:
    print(elem)
for elem in bg:
    print(elem)
