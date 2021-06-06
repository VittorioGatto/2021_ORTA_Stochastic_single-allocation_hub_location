# -*- coding: utf-8 -*-
import time
import logging
import gurobipy as gp
import numpy as np
from gurobipy import GRB


class StochasticSaphlp():
    def init(self):
        pass

    def solve(self, dict_data, sam, n_scenarios, time_limit=None, gap=None, verbose=False):
        nodes = range(dict_data['n_nodes'])
        scenarios = range(n_scenarios)

        problem_name = "StohasticSaphlp"
        logging.info("{}".format(problem_name))

        model = gp.Model(problem_name)
        Z = model.addVars(dict_data['n_nodes'], lb=0, ub=1, vtype=GRB.INTEGER, name='Z')
        X = model.addVars(dict_data['n_nodes'], dict_data['n_nodes'], n_scenarios, lb=0, ub=1, vtype=GRB.INTEGER, name='X')

        # objective function 1st stage
        obj_funct = gp.quicksum(dict_data['f'][i] * Z[i] for i in nodes)

        # # objective function 2nd stage - 1st term
        # for s in scenarios:
        #     temp = 0
        #     for i in nodes:
        #         for k in nodes:
        #             if i != k:
        #                 temp = sam.c[i, k, s] * X[i, k, s]
        #     obj_funct += temp / n_scenarios
        #
        # # objective function 2nd stage - 2nd term
        # for s in scenarios:
        #     A = 0
        #     B = 0
        #     C = 0
        #     D = 0
        #     s_term = 0
        #
        #     for i in nodes:
        #         for j in nodes:
        #             A = dict_data['d'][i, j] * Z[i] * Z[j]
        #
        #             for l in nodes:
        #                 if l != j:
        #                     B += dict_data['d'][i, l] * Z[i] * X[j, l, s]
        #
        #             for k in nodes:
        #                 if i != k:
        #                     C += dict_data['d'][k, j] * X[i, k, s] * Z[j]
        #
        #             for l in nodes:
        #                 for k in nodes:
        #                     if i != k:
        #                         if j != l:
        #                             D += (dict_data['d'][k, l] * X[i, k, s] * X[j, l, s])
        #
        #             s_term = dict_data['alpha'] * sam.w[i, j, s] * (A + B + C + D)
        #     obj_funct += s_term / n_scenarios

        model.setObjective(obj_funct, GRB.MINIMIZE)

        # constraint equation 25
        for s in scenarios:
            for i in nodes:
                sum_constr = 0
                for k in nodes:
                    if i != k:
                        sum_constr += X[i, k, s]
                model.addConstr(sum_constr == (1 - Z[i]), f"only _one_hubs{s}")

        # constraint equation 26
        for s in scenarios:
            for i in nodes:
                for k in nodes:
                    if k != i:
                        model.addConstr(X[i, k, s] <= Z[k], f"nodes_no connected{i,k,s}")


        # sum_constr = 0
        # for i in nodes:
        #     sum_constr += Z[i]
        # model.addConstr(sum_constr >= 1)

        model.update()
        if gap:
            model.setParam('MIPgap', gap)
        if time_limit:
            model.setParam(GRB.Param.TimeLimit, time_limit)
        if verbose:
            model.setParam('OutputFlag', 1)
        else:
            model.setParam('OutputFlag', 0)
        model.setParam('LogFile', './logs/gurobi.log')
        # model.write("./logs/model.lp")

        start = time.time()
        model.optimize()
        end = time.time()
        comp_time = end - start

        solZ = np.zeros(shape=dict_data['n_nodes'])
        solX = np.zeros(shape=(dict_data['n_nodes'], dict_data['n_nodes'], n_scenarios))

        of = -1

        if model.status == GRB.Status.OPTIMAL:
            for k in nodes:
                grb_var1 = model.getVarByName(f"Z[{k}]")
                solZ[k] = grb_var1.X
            for s in scenarios:
                for i in nodes:
                    for k in nodes:
                        grb_var2 = model.getVarByName(f"X[{i},{k},{s}]")
                        solX[i, k, s] = grb_var2.X
            of = model.getObjective().getValue()

        return of, solZ, solX, comp_time
