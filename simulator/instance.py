# -*- coding: utf-8 -*-
import logging
import numpy as np
from math import *

#Random generation DATA

class Instance:
    def __init__(self, sim_setting):
        logging.info("starting simulation...")

        # number of nodes
        self.n_nodes = sim_setting['n_nodes']

        # constants chi-alpha-sigma
        self.alpha = sim_setting['alpha']
        self.chi = sim_setting['chi']
        self.sigma = sim_setting['sigma']

        # f is the fixed cost of the hub node
        self.f = np.around(np.random.uniform(sim_setting['low_cost_fixed'], sim_setting['high_cost_fixed'],
                                             sim_setting['n_nodes']))

        # random creation of x and y coordinates
        x = np.around(np.random.uniform(sim_setting['low_d'], sim_setting['high_d'],
                                             size=(sim_setting['n_nodes'])))
        y = np.around(np.random.uniform(sim_setting['low_d'], sim_setting['high_d'],
                                             size=(sim_setting['n_nodes'])))

        self.d = np.zeros(shape=(self.n_nodes, self.n_nodes))

        # create from coordinates distance value
        for i in range(self.n_nodes):
            for j in range(self.n_nodes):
                self.d[i, j] = sqrt(pow((x[i] - x[j]), 2) + pow((y[i] - y[j]), 2))

        # set the coordinates to be passed to plot_results.py
        self.xcoord = x.copy()
        self.ycoord = y.copy()

        # self.d = (self.d + self.d.T) / 2
        # np.fill_diagonal(self.d, 0)

        self.w = np.around(np.random.uniform(sim_setting['low_w'], sim_setting['high_w'], size=(sim_setting['n_nodes'], sim_setting['n_nodes'])))



    def get_data(self):
        logging.info("getting data from instance...")
        return {
            "n_nodes": self.n_nodes,
            "f": self.f,
            "d": self.d,
            "alpha": self.alpha,
            "chi": self.chi,
            "sigma": self.sigma,
            "x": self.xcoord,
            "y": self.ycoord
        }
