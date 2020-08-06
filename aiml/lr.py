#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Realisation of Multivariate Linear Regression powered by pure Numpy.
Inspired by Machine Learning class from Andrew Ng at Coursera.
@see https://www.coursera.org/learn/machine-learning

FAQ:
- Linear Regression model looks like: y = theta0 + theta1*x1 + theta2*x2 ... thetan*xn
- We try to find theta parameters
- We use Gradient Descent for that
- It is very handful do np.seterr(all='raise') before using this module, to stop on any errors and avoid further
calculations that already wrong
"""
import numpy as np


def compute_cost(x: np.ndarray, y: np.ndarray, theta: np.ndarray) -> float:
    """Calculate and return cost function value (float scalar), based on given training set x, expected outcomes y and
    theta

    If x.shape = (m, n), then y.shape must be (m, 1) and theta.shape must be (1, n)

    :param x: set of features
    :param y: set of training examples
    :param theta: parameters of linear regression function

    """
    m = len(y)  # number of training examples
    return np.ndarray.item(sum(np.square(x @ theta - y)) / (2 * m))
