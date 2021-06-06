# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt


def plot_results(Z, X, n_scenarios):
    for s in range(n_scenarios):

        sol = X[:, :, s].copy()

        # distances based on the d matrix in instance.py
        distances = nx.from_numpy_matrix(inst.d)
        positions = nx.spring_layout(distances, seed=10)

        # multiplier to enlarge the nodes
        pi = 2
        # size of the nodes proportional to the OUTGOING FLOW
        mapped0_flow = sam.O_flow[:, s] * pi

        for i in range(inst.n_nodes):
            for j in range(inst.n_nodes):
                sol[i, j] = sol[i, j]*inst.d[i, j]

        net = nx.from_numpy_matrix(sol)

        color_map = []
        for i in range(inst.n_nodes):
            if Z[i] == 0:
                color_map.append('cyan')
            else:
                color_map.append('yellow')

        # printing of Z vector
        title = 'Plot Scenario n:' + str(s)
        plt.title(title)
        nx.draw(net, pos=positions, node_size=mapped0_flow, node_color=color_map, with_labels=True)
        limits = plt.axis('on')  # turns on axis
        plt.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        plt.legend()
        plt.show()
