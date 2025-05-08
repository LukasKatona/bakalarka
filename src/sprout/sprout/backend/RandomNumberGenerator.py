"""
This file contains the RandomNumberGenerator class, which is used to generate random numbers.
It is important to have a single static instance of the random number generator to ensure that the random numbers are generated in a consistent manner.

:author: Lukas Katona
"""

import numpy as np

class RandomNumberGenerator:
    # Static variables
    _rng = np.random.default_rng()

    # METHODS
    @staticmethod
    def exponential(scale = 1.0, size: int = None) -> np.ndarray | float:
        """
        Generate random numbers from an exponential distribution.

        :param scale: The scale parameter, which is the inverse of the rate parameter (lambda), defaults to 1.0
        :type scale: float, optional
        :param size: The number of random numbers to generate, defaults to None (single value)
        :type size: int, optional
        :return: Random numbers from the exponential distribution. If size is None, a single float is returned; otherwise, an array of floats is returned.
        :rtype: np.ndarray | float
        """
        return RandomNumberGenerator._rng.exponential(scale=scale, size=size)
    
    def uniform(low = 0.0, high = 1.0, size: int = None) -> np.ndarray | float:
        """
        Generate random numbers from a uniform distribution.

        :param low: Lower boundry, defaults to 0.0
        :type low: float, optional
        :param high: Upper boundry, defaults to 1.0
        :type high: float, optional
        :param size: The number of random numbers to generate, defaults to None
        :type size: int, optional
        :return: Random numbers from the uniform distribution. If size is None, a single float is returned; otherwise, an array of floats is returned.
        :rtype: np.ndarray | float
        """
        return RandomNumberGenerator._rng.uniform(low=low, high=high, size=size)
    
    def integers(low = 0, high = 1, size: int = None) -> np.ndarray | int:
        """
        Generate random integers from a uniform distribution.

        :param low: Lower boundry, defaults to 0
        :type low: int, optional
        :param high: Upper boundry, defaults to 1
        :type high: int, optional
        :param size: The number of random integers to generate, defaults to None
        :type size: int, optional
        :return: Random integers from the uniform distribution. If size is None, a single integer is returned; otherwise, an array of integers is returned.
        :rtype: np.ndarray | int
        """
        return int(RandomNumberGenerator._rng.integers(low=low, high=high, size=size))