import numpy as np
import unittest
import aiml.lr as lr


class TestLinearRegression(unittest.TestCase):
    def test_compute_cost(self):
        """Testing Linear Regression compute_cost() function. Expected results were given from Octave"""
        x = np.array([[1.0,  0.13000986907454054053, -0.22367518716859130512],
                      [1.0, -0.50418983822317686716, -0.22367518716859130512]])
        y = np.array([[399900],
                      [329900]])

        theta = np.zeros(shape=(3, 1))
        expected_j = 67188505000.0
        j = lr.compute_cost(x, y, theta)
        self.assertAlmostEqual(j, expected_j)

        theta = np.ones(shape=(3, 1))
        expected_j = 67188278890.0
        j = lr.compute_cost(x, y, theta)
        self.assertAlmostEqual(j, expected_j, places=0)

        theta[0, 0] = 89597.909542
        theta[1, 0] = 139.210674
        theta[2, 0] = -8738.019112
        expected_j = 37977534204.0
        j = lr.compute_cost(x, y, theta)
        self.assertAlmostEqual(j, expected_j, places=0)

        theta[0, 0] = 335910.396042
        theta[1, 0] = 100867.715540
        theta[2, 0] = 2874.680525
        expected_j = 1180860698
        j = lr.compute_cost(x, y, theta)
        self.assertAlmostEqual(j, expected_j, places=1)
