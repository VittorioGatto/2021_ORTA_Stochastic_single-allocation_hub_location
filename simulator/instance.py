# -*- coding: utf-8 -*-
import logging
import numpy as np


class Instance():
    def __init__(self, sim_setting):
        logging.info("starting simulation...")

        self.n_nodes = sim_setting['n_nodes']

        self.cost = np.around(np.random.uniform(sim_setting['low_cost'], sim_setting['high_cost'],
                                                sim_setting['n_nodes']))

        self.max_distance = sim_setting['high_distance']
        self.distance = np.around(np.random.uniform(sim_setting['low_distance'], sim_setting['high_distance'],
                                                    sim_setting['n_nodes']))

        self.O_flow = np.around(np.random.uniform(sim_setting['low_flow'], sim_setting['high_flow'],
                                                  sim_setting['n_nodes']))

        self.D_flow = np.around(np.random.uniform(sim_setting['low_flow'], sim_setting['high_flow'],
                                                  sim_setting['n_nodes']))

        logging.info(f"n_nodes: {self.n_nodes}")
        logging.info(f"cost: {self.cost}")
        logging.info(f"max_distance: {self.max_distance}")
        logging.info(f"distance: {self.distance}")
        logging.info(f"O_flow: {self.O_flow}")
        logging.info(f"D_flow: {self.D_flow}")

        logging.info("simulation end")

    def get_data(self):
        logging.info("getting data from instance...")
        return {
            "n_nodes": self.n_nodes,
            "cost": self.cost,
            "max_distance": self.max_distance,
            "distance": self.distance,
            "O_flow": self.O_flow,
            "D_flow": self.D_flow,
        }
