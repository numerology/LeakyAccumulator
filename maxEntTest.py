__author__ = 'Jiaxiao Zheng'

import numpy as np
from maxEntropySolve import *
import random

#Define constant
N = 4
A = 3
B = 3

numOfIteration = 11
lamb = 10 #weight for reward

px = {}
truePy = {}
reward = {}

featG = {}
featH = {} #deprecated for a while


for t in range(0,N):
    for xSeqNum in range(0,A**(t-1)):
        for ySeqNum in range(0,B**(t-1)):
            for xt in range(0,A):
                px[(str(xt),str(xSeqNum),str(ySeqNum))] = 1/A


#define reward and features
for xSeqNum in range(0,A**N):
    for ySeqNum in range(0,B**N):
        reward[(str(xSeqNum), str(ySeqNum))] = 1 if str(ySeqNum)[N-1]==0 else 0
        featG[(str(xSeqNum), str(ySeqNum))] = 1 if xSeqNum == ySeqNum else 0
        featH[(str(xSeqNum), str(ySeqNum))] = 0
'''
Now define the Leaky Accumulatro model
Reference: Usher, Marius, and James L. McClelland. "The time course of perceptual choice: the leaky, competing accumulator model."
Psychological review 108.3 (2001): 550.

'''
# M is the matrix for coupling effect. Play with different suppressing model later
M = 0.15 * np.asmatrix(np.ones([A,A])) - 0.75 * np.diag(np.ones(A))
sigma = 0.1
unit = -10

c = 1
for xSeqNum in range(0,A**N):
    xSeq = str(xSeqNum)
    acc = np.zeros(A)
    for t in range(0,N):
        acc[xSeq[t]] += unit
        sumofsm = np.sum(np.exp(c * acc))
        for ySeqNum in range(0,B**(t-1)):
            for yt in range(0,B):
                truePy[(str(yt), xSeqNum[0:t+1], str(ySeqNum))] = np.exp(c*acc[yt])/sumofsm

        acc = acc - np.dot(np.asmatrix(acc), M)
        acc = np.clip(acc, a_min = 0, a_max = 65535)

currentEG = np.zeros(numOfIteration)
trueEG = np.zeros(numOfIteration)
currentEnt = np.zeros(numOfIteration)
currentJointEnt = np.zeros(numOfIteration)
sumOfFunc = np.zeros(numOfIteration)

for iter in range(0,numOfIteration,2):
    result = maxEntropySolve(N, A = A, B = B, G = featG, H = featH, eqCons = 1, neqCons=1, px = px, truePy = truePy, delta = 0.00001, stepSize=0.001)

    for xSeqNum in range(0,A**N):
        for ySeqNum in range(0,B**N):
            xSeq = str(xSeqNum)
            ySeq = str(ySeqNum)

            currentJoint = 1
            currentCausalX = 1
            for i in range(0,N):


