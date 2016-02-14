__author__ = 'jxzheng'

#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random


'''
The format of the causal cond distribution was assigned as dictionary with key in the forms of tuples:
P(X_t | X_{1:t-1}, M_{1:t-1}) = px[(X_t,'X_{1:t-1}','M_{1:t-1}')]

Z and py will parallel this
'''
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

    lamb = np.random.rand(1,eqCons)
    gamma = np.random.rand(1,neqCons)

    Z = {}
    py = {}

    cnt = 0
    nextlamb = -1
    nextgamma = -1

    #compute the expectation of G
    trueEG = 0
    for xSeqNum in range(0,A**N):
        for ySeqNum in range(0,B**N):
            xSeq = str(xSeqNum)
            ySeq = str(ySeqNum)

            currentJoint = 1
            for i in range(0,N):
                currentJoint = currentJoint * px[()]

    return {'dual':None, 'py':None}



