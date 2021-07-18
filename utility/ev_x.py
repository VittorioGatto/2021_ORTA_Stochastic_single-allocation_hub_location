import numpy as np

# Evaluation of the X matrix with respect to the Z vector solution we provide
def ev_x(nodes, d, sol_z, sol_x, s):

    # Evaluation of X with d
    newD = np.zeros((nodes, nodes))

    for j in range(nodes):
        for i in range(nodes):
            newD[i, j] = d[i, j] * sol_z[i]

    # we select the links with minimum distance from each other
    for i in range(nodes):
        if sol_z[i] != 1:
            arr = np.ma.MaskedArray(newD[:, i], newD[:, i] <= 0)
            sol_x[i, np.ma.argmin(arr), s] = 1

    return sol_x