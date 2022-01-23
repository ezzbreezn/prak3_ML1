class WordContextGenerator:
    def __init__(self, words, window_size):
        self.words = words
        self.window_size = window_size
        self.size = len(words)

    def __iter__(self):
        i = 0
        j = -self.window_size
        while i < self.size:
            while j <= self.window_size:
                if i + j < 0 or j == 0:
                    j += 1
                    continue
                if i + j >= self.size:
                    break 
                yield (self.words[i], self.words[i + j])
                j += 1
            i += 1
            j = -self.window_size
