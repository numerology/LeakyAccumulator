__author__ = 'jxzheng'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

def maxEntropySolve(N, G, H, eqCons, neqCons, px, truePy, A, B, stepSize, delta):
    #N: length of sequence
    #G, H: dicts indicating features
    #eqCons, neqCons: number of equality constraints and nonequality constraints
    #px: dicts indicating the causal cond distribution of x
    #truePy: dicts indicating true causal cond distribution of y
    #A, B: cardinality of possible actions
    #stepsize: stepsize of dual vars
    #delta: convergence tolerance

    #Initialize dual vars

    lamb = np.random.rand(1,N)
    gamma = np.random.rand(1,N)

    Z = np.ones(shape = [B*N, A**N, B**(N-1)])
    py = np.zeros(shape = [B*N, A**N, B**(N-1)])

    cnt = 0
    nextlamb = -1
    nextgamma = -1

    #compute the expectation of G
    trueEG = 0
    for

    return {'dual':None, 'py':None}



