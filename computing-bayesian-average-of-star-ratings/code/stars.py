# stars
# Ranks the MovieLens data set by star rating.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Aug 28 16:32:47 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: stars.py [] benjamin@bengfort.com $

"""
Ranks the MovieLens data set by star rating.
"""

##########################################################################
## Imports
##########################################################################

import os
import heapq

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from collections import Counter
from operator import itemgetter

##########################################################################
## Module Constants
##########################################################################

BASE  = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
PATH  = os.path.join(BASE, "data", "ratings.csv")
PRIOR = [2, 2, 2, 2, 2]

##########################################################################
## Analysis Object
##########################################################################

class Ratings(object):
    """
    An analytical wrapper that manages access to the data and wraps various
    statistical functions for easy and quick evaluation.
    """

    def __init__(self, path=PATH, m=None, C=None):
        self.path  = path
        self.prior = m
        self.confidence = C
        self.load()

    def load(self):
        """
        Load data from disk into a DataFrame.
        """
        self.data = pd.DataFrame(pd.read_csv(self.path))

    def bayesian_mean(self, arr):
        """
        Computes the Bayesian mean from the prior and confidence.
        """
        if not self.prior or not self.confidence:
            raise TypeError("Bayesian mean must be computed with m and C")

        return (self.confidence * self.prior + arr.sum()) / (self.confidence + arr.count())

    def dirichlet_mean(self, arr, prior=PRIOR):
        """
        Computes the Dirichlet mean with a prior.
        """
        counter   = Counter(arr)
        votes     = [val[1] for val in
                     sorted(counter.items(), key=itemgetter(0))]
        posterior = map(sum, zip(votes, prior))
        N         = sum(posterior)
        weights   = map(lambda i: (i[0]+1)*i[1], enumerate(posterior))

        return float(sum(weights)) / N

    @property
    def movies(self):
        """
        Returns the data grouped by Movie
        """
        return self.data.groupby('title')

    def get_means(self):
        return self.movies['rating'].mean()

    def get_counts(self):
        return self.movies['rating'].count()

    def get_bayesian_estimates(self):
        return self.movies['rating'].agg(self.bayesian_mean)

    def get_dirichlet_estimates(self):
        return self.movies['rating'].agg(self.dirichlet_mean)

    def top_movies(self, n=10):
        grid   = pd.DataFrame({
                    'mean':  self.get_means(),
                    'count': self.get_counts(),
                    'bayes': self.get_bayesian_estimates(),
                    'dirichlet': self.get_dirichlet_estimates()
                 })
        return grid.ix[grid['dirichlet'].argsort()[-n:]]

    def plot_mean_frequency(self):
        grid   = pd.DataFrame({
                    'Mean Rating':  self.movies['rating'].mean(),
                    'Number of Reviewers': self.movies['rating'].count()
                 })

        grid.plot(x='Number of Reviewers', y='Mean Rating', kind='hexbin',
                  xscale='log', cmap='YlGnBu', gridsize=12, mincnt=1,
                  title="Star Ratings by Simple Mean")
        plt.show()

    def describe(self):
        return self.data.describe()

    def __str__(self):
        return str(self.data.head())

if __name__ == '__main__':
    ratings = Ratings(m=3.25, C=50)
    print ratings.describe()
    print ratings.top_movies()
    print ratings.plot_mean_frequency()
