# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt


def plot_results(inst, sam, Z, X, n_scenarios):
    for s in range(n_scenarios):

        sol = X[:, :, s].copy()

        # # distances based on the d matrix in instance.py
        # distances = nx.from_numpy_matrix(inst.d)
        # positions = nx.spring_layout(distances, seed=10)
        pos = {}
        for i in range(inst.n_nodes):
            pos.update({i: (inst.xcoord[i], inst.ycoord[i])})

        # multiplier to enlarge the nodes
        pi = 2
        # size of the nodes proportional to the OUTGOING FLOW
        mapped0_flow = sam.O_flow[:, s] * pi

        # creation of the graph from the X matrix
        net = nx.from_numpy_matrix(sol)

        color_map = []
        for i in range(inst.n_nodes):
            if Z[i] == 0:
                color_map.append('cyan')
            else:
                color_map.append('yellow')

        # printing of the results
        title = 'Plot Scenario n:' + str(s)
        plt.title(title)
        nx.draw(net, pos=pos, node_size=mapped0_flow, node_color=color_map, with_labels=True)
        plt.axis('on')  # turns on axis
        plt.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        plt.legend()
        plt.show()
