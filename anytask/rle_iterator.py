import numpy as np


def encode_rle(x):
    if x.size == 0:
        return (None, None)
    else:
        cond = x[1:] != x[:-1]
        idx = np.append(np.where(cond), x.size - 1)
        times = np.diff(np.append(-1, idx))
        return (x[idx], times)


class RleSequence:
    def __init__(self, input_sequence):
        self.values, self.times = encode_rle(input_sequence)
        self.len = np.sum(self.times)

    def __getitem__(self, pos):
        if type(pos) is int:
            if pos < 0:
                pos += np.sum(self.times)
            idx = 0
            temp_times = self.times[idx]
            while pos > 0:
                temp_times -= 1
                if temp_times == 0:
                    idx += 1
                    temp_times = self.times[idx]
                pos -= 1
            return self.values[idx]
        elif type(pos) is slice:
            idxs = list(range(*pos.indices(np.sum(self.times))))
            ans = np.zeros(len(idxs))
            ans_idx = 0
            p = 0
            if len(idxs) == 0:
                return np.array([])
            if idxs[0] <= idxs[-1]:
                step = 1
            else:
                step = -1
            length = len(idxs)
            for i in range(length):
                if i == 0:
                    idx = 0
                    temp_times = self.times[idx]
                    while p < idxs[i]:
                        temp_times -= 1
                        if temp_times == 0:
                            idx += 1
                            temp_times = self.times[idx]
                        p += 1
                else:
                    if step < 0:
                        temp_times = self.times[idx] - temp_times
                    while p != idxs[i]:
                        temp_times -= 1
                        if temp_times == 0:
                            idx += step
                            temp_times = self.times[idx]
                        p += step
                ans[ans_idx] = self.values[idx]
                ans_idx += 1
            return ans.astype('int64')

    def __iter__(self):
        self.indx = -1
        self.true_indx = 0
        self.temp_times = 0
        return self

    def __next__(self):
        self.indx += 1
        if self.indx >= self.len:
            raise StopIteration
        self.temp_times += 1
        if self.temp_times > self.times[self.true_indx]:
            self.true_indx += 1
            self.temp_times = 1
        return self.values[self.true_indx]
