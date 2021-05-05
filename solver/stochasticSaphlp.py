# -*- coding: utf-8 -*-
import time
import logging
import gurobipy as gp
from gurobipy import GRB


class StochasticSaphlp():
    def __init__(self):
        pass

    def solve(self, dict_data, reward, n_scenarios, time_limit=None, gap=None, verbose=False):
        items = range(dict_data['n_items'])
        scenarios = range(n_scenarios)

        problem_name = "StohasticSaphlp"
        logging.info("{}".format(problem_name))


        model = gp.Model(problem_name)
        X = model.addVars(dict_data['n_nodes'], dict_data['n_nodes'], lb=0, ub=1, vtype=GRB.INTEGER, name='X')
        Y = model.addVars(dict_data['n_nodes'], n_scenarios, lb=0, ub=1, vtype=GRB.INTEGER, name='Y')

        obj_funct = gp.quicksum(dict_data["cost"][i] * X[i] for i in items)
        # for s in scenarios:
        #     obj_funct += gp.quicksum(reward[i, s] * Y[i, s] for i in items)/(n_scenarios + 0.0)
        obj_funct += gp.quicksum(reward[i, s] * Y[i, s] for i in items for s in scenarios) / (n_scenarios + 0.0)
        model.setObjective(obj_funct, GRB.MAXIMIZE)

        model.addConstr(gp.quicksum(X[i] for i in items) == 1)
        model.addConstr(gp.quicksum(X[i] for i in items) <= X[k][k])

        for s in scenarios:
            model.addConstr(
                gp.quicksum(dict_data['flow'][i] * Y[i, s] for i in items) <= dict_data['max_flow'],
                f"volume_limit_ss_{s}"
            )
        for i in items:
            model.addConstr(
                gp.quicksum(Y[i, s] for s in scenarios) <= n_scenarios * X[i],
                f"link_X_Y_for_item_{i}"
            )
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
            for i in items:
                grb_var = model.getVarByName(
                    f"X[{i}]"
                )
                sol[i] = grb_var.X
            of = model.getObjective().getValue()
        return of, sol, comp_time
