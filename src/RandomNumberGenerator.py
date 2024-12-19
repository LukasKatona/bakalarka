import numpy as np

class RandomNumberGenerator:
    _rng = np.random.default_rng()

    @staticmethod
    def exponential(scale=1.0, size=None):
        return RandomNumberGenerator._rng.exponential(scale=scale, size=size)