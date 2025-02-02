import numpy as np

class RandomNumberGenerator:
    # Static variables
    _rng = np.random.default_rng()

    # METHODS
    @staticmethod
    def exponential(scale=1.0, size=None):
        return RandomNumberGenerator._rng.exponential(scale=scale, size=size)
    
    def uniform(low=0.0, high=1.0, size=None):
        return RandomNumberGenerator._rng.uniform(low=low, high=high, size=size)
    
    def integers(low=0, high=1, size=None):
        return int(RandomNumberGenerator._rng.integers(low=low, high=high, size=size))