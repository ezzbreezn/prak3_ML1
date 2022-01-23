class Polynomial:
    def __init__(self, *coeff):
        self.coeff = coeff

    def __call__(self, x):
        ans = 0
        for c in self.coeff[::-1]:
            ans = ans * x + c
        return ans
