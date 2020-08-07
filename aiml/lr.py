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


def gradient_descent(x: np.ndarray, y: np.ndarray, theta: np.ndarray, alpha: float, num_iters: int) \
        -> (np.ndarray, np.ndarray):
    """Straitforward (unoptimized) version of Gradient Descent. Applies num_iters iterations with learning rate alpha
    and returns tuple (theta, J_history) with finded theta and history of values of the cost function J_history

    If x.shape = (m, n), then y.shape must be (m, 1) and theta.shape must be (1, n)

    :param x: set of features
    :param y: set of training examples
    :param theta: parameters of linear regression function
    :param alpha: learning rate alpha (size of the one step of gradient descent)
    :param num_iters: number of iterations for gradient descent
    :return: a tuple (theta, J_historu), where theta is sought-for parameter of Linear Regression Model,
        J_history - is an array of cost function values over iterations
    """
    m = len(y)  # number of training examples
    n = x.shape[1]  # number of features
    j_history = np.zeros(shape=(num_iters, 1))
    for i in range(num_iters):
        for j in range(n):
            # np.multiply is the element-wise multiplication
            theta[j, 0] = theta[j, 0] - alpha * sum(np.multiply(x @ theta - y, x[:, j].reshape(m, 1))) / m
        j_history[i] = compute_cost(x, y, theta)
    return theta, j_history


def gd(x: np.ndarray, y: np.ndarray, theta: np.ndarray, alpha: float, num_iters: int) \
        -> (np.ndarray, np.ndarray):
    """Optimized version of gradient_descent function. Parameters and return is equal with gradient_descent()"""
    m = len(y)  # number of training examples
    n = x.shape[1]  # number of features
    alpha_m = alpha / m  # constant formula part, calculate outside of loops
    j_history = np.zeros(shape=(num_iters, 1))
    for i in range(num_iters):
        difference = x @ theta - y
        for j in range(n):
            # np.multiply is the element-wise multiplication
            theta[j, 0] = theta[j, 0] - alpha_m * sum(np.multiply(difference, x[:, j].reshape(m, 1)))
        j_history[i] = np.ndarray.item(sum(np.square(difference)) / (2 * m))  # use precalculated difference
    return theta, j_history
