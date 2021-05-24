# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt


def plot_results(Z, X, n_scenarios):
    for s in range(n_scenarios):
            sol = X[:, :, s].copy()
            net = nx.from_numpy_matrix(sol)
            nx.draw(net)
            plt.show()

