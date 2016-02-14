__author__ = 'jxzheng'

#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random


'''
X moves first, then Y
The format of the causal cond distribution was assigned as dictionary with key in the forms of tuples:
P(X_t | X_{1:t-1}, Y_{1:t-1}) = px[(X_t,'X_{1:t-1}','Y_{1:t-1}')]
P(Y_t | X_{1:t}, Y_{1:t-1}) = px[(Y_t,'X_{1:t}','Y_{1:t-1}')]
Z will parallel this
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

    #TODO: inconsistency: value of G or H should be array, not scalar. Check multiplications

    lamb = np.random.rand(1,eqCons)
    gamma = np.random.rand(1,neqCons)

    Z = {}
    py = {}

    cnt = 0
    nextlamb = -np.ones(1,eqCons)
    nextgamma = -np.ones(1,neqCons)

    #compute the expectation of G, H
    trueEG = 0
    trueEH = 0
    for xSeqNum in range(0,A**N):
        for ySeqNum in range(0,B**N):
            xSeq = str(xSeqNum)
            ySeq = str(ySeqNum)

            currentJoint = 1
            for i in range(0,N):
                currentJoint = currentJoint * px[(xSeq[i], xSeq[0:i], ySeq[0:i])] * truePy[(ySeq[i], xSeq[0:i+1], ySeq[0:i])]

            trueEG += currentJoint * G[(xSeq, ySeq)]
            trueEH += currentJoint * H[(xSeq, ySeq)]

    while np.linalg.norm(nextlamb - lamb) + np.linalg.norm(nextgamma - gamma) > delta:
        if cnt > 0:
            lamb = nextlamb
            gamma = nextgamma

        for i in range(N-1,-1,-1):
            if i == N:
            #determining the last layer
                for xCondSeqNum in range(0, A**N):
                    for yCondSeqNum in range(0, B**(N-1)):
                        xCondSeq = str(xCondSeqNum)
                        yCondSeq = str(yCondSeqNum)

                        sumZ = 0
                        for yN in range(0, B):
                            Z[(str(yN), xCondSeq, yCondSeq)] = np.exp(lamb * G[(xCondSeq, yCondSeq + str(yN))] + gamma * H[(xCondSeq, yCondSeq + str(yN))])
                            sumZ += Z[(str(yN), xCondSeq, yCondSeq)]
                        for yN in range(0, B):
                            py[(str(yN), xCondSeq, yCondSeq)] = Z[(str(yN), xCondSeq, yCondSeq)]/sumZ

            else:
                for xCondSeqNum in range(0, A**i):
                    xCondSeq = str(xCondSeqNum)
                    for yCondSeqNum in range(0, B**(i-1)):
                        yCondSeq = str(yCondSeqNum)
                        sumZ = 0
                        for yN in range(0,B):
                            sumOverX = 0
                            for xNPlus1 in range(0,A):
                                sumOverY = 0
                                for yNPlus1 in range(0,B):
                                    sumOverY += Z[(str(yNPlus1), xCondSeq + str(xNPlus1), yCondSeq + str(yN))]

                                sumOverX += np.log(sumOverY) * px[(str(xNPlus1), xCondSeq, yCondSeq + str(yN))]

                            Z[(str(yN), xCondSeq, yCondSeq)] = np.exp(sumOverX)
                            sumZ += Z[(str(yN), xCondSeq, yCondSeq)]

                        for yN in range(0, B):
                            py[(str(yN), xCondSeq, yCondSeq)] = Z[(str(yN), xCondSeq, yCondSeq)] / sumZ

        #update dual vars
        eG = 0
        eH = 0
        for xSeqNum in range(0, A**N):
            for ySeqNum in range(0, B**N):
                xSeq = str(xSeqNum)
                ySeq = str(ySeqNum)

                currentJoint = 1
                for i in range(0,N):
                    currentJoint = currentJoint * px[(xSeq[i], xSeq[0:i], ySeq[0:i])] * py[(ySeq[i], xSeq[0:i+1], ySeq[0:i])]

                eG += currentJoint * G[(xSeq, ySeq)]
                eH += currentJoint * H[(xSeq, ySeq)]

        nextlamb = lamb - stepSize * (eG - trueEG)
        nextgamma = gamma - stepSize * (eH - trueEH) if gamma - stepSize * (eH - trueEH) > 0 else 0

        cnt += 1


    return {'dual':(lamb, gamma), 'py':py}



