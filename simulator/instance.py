# -*- coding: utf-8 -*-
import logging
import numpy as np


class Instance():
    def __init__(self, sim_setting):
        logging.info("starting simulation...")

        self.n_nodes = sim_setting['n_nodes']

        self.alpha = sim_setting['alpha']

        self.chi = sim_setting['chi']

        self.sigma = sim_setting['sigma']

        self.f = np.around(np.random.uniform(sim_setting['low_cost_fixed'], sim_setting['high_cost_fixed'],
                                             sim_setting['n_nodes']))

        self.max_d = sim_setting['high_d']
        self.d = np.around(np.random.uniform(sim_setting['low_d'], sim_setting['high_d'],
                                             size=(sim_setting['n_nodes'], sim_setting['n_nodes'])))
        self.d = (self.d + self.d.T) / 2
        np.fill_diagonal(self.d, 0)

        self.w = np.around(np.random.uniform(sim_setting['low_w'], sim_setting['high_w'],
                                             size=(sim_setting['n_nodes'], sim_setting['n_nodes'])))
        self.O_flow = self.w.sum(axis=1)
        self.D_flow = self.w.sum(axis=0)

        self.c = []
        for i in range(sim_setting['n_nodes']):
            row = []
            for k in range(sim_setting['n_nodes']):
                row.append(self.d[i][k] * (self.chi * self.O_flow[i] + self.sigma * self.D_flow[i]))
            self.c.append(row)

        logging.info(f"n_nodes: {self.n_nodes}")

    def get_data(self):
        logging.info("getting data from instance...")
        return {
            "n_nodes": self.n_nodes,
            "c": self.c,
            "f": self.f,
            "max_dd": self.max_d,
            "d": self.d,
            "O_flow": self.O_flow,
            "D_flow": self.D_flow,
            "alpha": self.alpha,
            "chi": self.chi,
            "sigma": self.sigma,
            "w": self.w

        }
