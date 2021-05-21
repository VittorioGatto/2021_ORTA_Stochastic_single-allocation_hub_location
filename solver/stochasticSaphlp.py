# -*- coding: utf-8 -*-
import time
import logging
import gurobipy as gp
from gurobipy import GRB


class StochasticSaphlp():
    def __init__(self):
        pass

    def solve(self, dict_data, sam, n_scenarios, time_limit=None, gap=None, verbose=False):
        nodes = range(dict_data['n_nodes'])
        scenarios = range(n_scenarios)

        problem_name = "StohasticSaphlp"
        logging.info("{}".format(problem_name))

        model = gp.Model(problem_name)
        Z = model.addVars(dict_data['n_nodes'], lb=0, ub=1, vtype=GRB.INTEGER, name='Z')
        X = model.addVars(dict_data['n_nodes'], dict_data['n_nodes'], n_scenarios, lb=0, ub=1, vtype=GRB.INTEGER,
                          name='X')

        # objective function 1st stage
        obj_funct = gp.quicksum(dict_data['f'][i] * Z[i] for i in nodes)

        # objective function 2nd stage - 1st term
        obj_funct += gp.quicksum(sam.c[i, k, s] * X[i, k, s] for i in nodes for k in nodes for s in scenarios) / (
                n_scenarios + 0.0)

        # objective function 2nd stage - 2nd term
        for s in scenarios:
            p_sum = 0
            K = 0
            L = 0
            f_term = 0
            s_term = 0
            for i in nodes:
                for j in nodes:
                    f_term = dict_data['d'][i, j] * Z[i] * Z[j]
                    for l in nodes:
                        for k in nodes:
                            if i != k and j != l:
                                PG = dict_data['d'][l, k] * X[i, l, s]
                                p_sum += PG * X[j, k, s]
                    for k in nodes:
                        if i != k:
                            K += dict_data['d'][k, j] * X[i, k, s] * Z[j]
                    for l in nodes:
                        if j != l:
                            L += (dict_data['d'][i, l] * Z[i] * X[j, l, s])
                    K = p_sum + K
                    L = L + K
                    f_term = f_term + L
                    s_term = dict_data['alpha'] * sam.w[i, j, s]
            obj_funct += s_term * f_term

        model.setObjective(obj_funct, GRB.MINIMIZE)

        # constraint equation 25
        for s in scenarios:
            for i in nodes:
                sum_constr = 0
                for k in nodes:
                    if i != k:
                        sum_constr += X[i, k, s]
                model.addConstr(sum_constr == 1-Z[i])

        # constraint equation26
        for s in scenarios:
            for k in nodes:
                for i in nodes:
                    if k != i:
                        model.addConstr(X[i,k,s]<=Z[k])

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

        sol = [0] * dict_data['n_items']
        of = -1

        if model.status == GRB.Status.OPTIMAL:
            for i in nodes:
                grb_var = model.getVarByName(f"X[{i}]")
                sol[i] = grb_var.X
            of = model.getObjective().getValue()
        return of, sol, comp_time
