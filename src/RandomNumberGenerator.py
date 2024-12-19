import numpy as np

class RandomNumberGenerator:
    # Static variables
    _rng = np.random.default_rng()

    # METHODS
    @staticmethod
    def exponential(scale=1.0, size=None):
        return RandomNumberGenerator._rng.exponential(scale=scale, size=size)