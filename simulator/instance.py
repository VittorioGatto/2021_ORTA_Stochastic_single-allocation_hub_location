# -*- coding: utf-8 -*-
import logging
import numpy as np


class Instance():
    def __init__(self, sim_setting):
        logging.info("starting simulation...")
        self.max_size = sim_setting['knapsack_size']
        self.sizes = np.around(np.random.uniform(
            sim_setting['low_size'],
            sim_setting['high_size'],
            sim_setting['n_items']
        ))
        self.profits = np.around(np.random.uniform(
            sim_setting['low_profit'],
            sim_setting['high_profit'],
            sim_setting['n_items']
        ), 2)
        self.n_items = sim_setting['n_items']

        self.sizes_ss = np.around(np.random.uniform(
            sim_setting['low_size'],
            sim_setting['high_size'],
            sim_setting['n_items']
        ))
        self.max_size_ss = sim_setting['knapsack_size']

        logging.info(f"max_size: {self.max_size}")
        logging.info(f"sizes: {self.sizes}")
        logging.info(f"profits: {self.profits}")
        logging.info(f"n_items: {self.n_items}")
        logging.info(f"sizes_ss: {self.sizes_ss}")
        logging.info(f"max_size_ss: {self.max_size_ss}")
        logging.info("simulation end")

    def get_data(self):
        logging.info("getting data from instance...")
        return {
            "profits": self.profits,
            "sizes": self.sizes,
            "max_size": self.max_size,
            "n_items": self.n_items,
            "sizes_ss": self.sizes_ss,
            "max_size_ss": self.max_size_ss,
        }
