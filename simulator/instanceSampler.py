import numpy as np
from math import *


class InstanceSampler:
    def __init__(self, filename):
        fp = open(filename, 'r')

        # read the number of nodes
        self.n_nodes = int(fp.readline())

        x = []
        y = []

        # read the value of the coordinates
        for i in range(self.n_nodes):
            v = fp.readline().split()
            x.append(float(v[0]))
            y.append(float(v[1]))

        self.d = np.zeros(shape=(self.n_nodes, self.n_nodes))

        # create from coordinates distance value
        for i in range(self.n_nodes):
            for j in range(self.n_nodes):
                self.d[i, j] = sqrt(pow((x[i] - x[j]), 2) + pow((y[i] - y[j]), 2))

        self.w = np.zeros([self.n_nodes, self.n_nodes])

        # take the flow
        for i in range(self.n_nodes):
            flow = fp.readline().split()
            for j in range(self.n_nodes):
                self.w[i, j] = float(flow[j])

        # value that we don't consider
        fp.readline()

        # read the constants chi-alpha-sigma
        self.chi = float(fp.readline())
        self.alpha = float(fp.readline())
        self.sigma = float(fp.readline())

        # read the fixed costs of the nodes
        self.f = np.zeros([self.n_nodes])
        for i in range(self.n_nodes):
            self.f[i] = float(fp.readline())

        # set the coordinates to be passed to plot_results.py
        self.xcoord = x.copy()
        self.ycoord = y.copy()

        fp.close()

    def get_data(self):

        return {
            "n_nodes": self.n_nodes,
            "f": self.f,
            "d": self.d,
            "alpha": self.alpha,
            "chi": self.chi,
            "sigma": self.sigma,
            "w": self.w,
            "x": self.xcoord,
            "y": self.ycoord
        }