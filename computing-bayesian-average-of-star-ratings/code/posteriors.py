# posteriors
# Compute the likelihood of posteriors
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Sep 09 16:15:32 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: posteriors.py [] benjamin@bengfort.com $

"""
Compute the likelihood of posteriors
"""

##########################################################################
## Imports
##########################################################################

import random
import numpy as np
import matplotlib.pyplot as plt

def random_observations(x=0.68, n=100):
    for i in xrange(n):
        if random.random() > x:
            yield 0
        else:
            yield 1

def posterior(x, k, n):
    """
    Returns the posterior probability for x given k and n
    """
    return (x**k)*((1-x)**(n-k))

def graph(observations):
    """
    Graphs the refining posterior for our observations
    """

    x = np.arange(0.0, 1.0, 0.01)

    for i, n in enumerate((1, 5, 10, 25, 50, 100)):
        k = sum(observations[:n])
        print "k=%i after %i observations" % (k,n)

        axe = plt.subplot(2, 3, i+1)
        axe.set_title("K=%i, N=%i" % (k,n))
        if i > 2: axe.set_xlabel("Value of X")
        if i == 0 or i==3: axe.set_ylabel("Probability of Posterior")
        #axe.get_yaxis().set_ticks([])
        axe.plot(x, posterior(x, k, n))

    plt.suptitle("Improving Posterior with more Observations")
    plt.show()

if __name__ == '__main__':
    observations = list(random_observations())
    graph(observations)
