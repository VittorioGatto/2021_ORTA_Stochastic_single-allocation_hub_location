# -*- coding: utf-8 -*-
import os
import time
import logging
import json
import numpy as np
import gurobipy as gp
from gurobipy import GRB


class Tester():
    def __init__(self):
        pass

    def compare_sols_lst(
        self, inst, sampler, sols, labels, n_scenarios
    ):
        ans_dict = {}
        reward = sampler.sample_stoch(
            inst,
            n_scenarios=n_scenarios
        )
        for j in range(len(sols)):
            profit_raw_data = self.solve_second_stages(
                inst, sols[j],
                n_scenarios, reward
            )
            ans_dict[labels[j]] = profit_raw_data

        return ans_dict

    def solve_second_stages(
        self, inst, sol, n_scenarios, reward
    ):
        ans = []
        obj_fs = 0
        for i in range(inst.n_items):
            obj_fs += inst.profits[i] * sol[i]
        items = range(inst.n_items)
        for s in range(n_scenarios):
            problem_name = "SecondStagePrb"
            model = gp.Model(problem_name)
            Y = model.addVars(
                inst.n_items,
                lb=0,
                ub=1,
                vtype=GRB.INTEGER,
                name='Y'
            )

            obj_funct = gp.quicksum(reward[i, s] * Y[i] for i in items)

            model.setObjective(obj_funct, GRB.MAXIMIZE)
            
            model.addConstr(
                gp.quicksum(inst.sizes_ss[i] * Y[i] for i in items) <= inst.max_size_ss,
                f"volume_limit_ss"
            )
            for i in items:
                model.addConstr(
                    Y[i] <= sol[i],
                    f"link_X_Y_for_item_{i}"
                )
            model.update()
            model.setParam('OutputFlag', 0)
            model.setParam('LogFile', './logs/gurobi.log')
            model.optimize()
            ans.append(obj_fs + model.getObjective().getValue())

        return ans

    def in_sample_stability(self, problem, sampler, instance, n_repertions, n_scenarios_sol):
        ans = [0] * n_repertions
        for i in range(n_repertions):
            reward = sampler.sample_stoch(
                instance,
                n_scenarios=n_scenarios_sol
            )
            of, sol, comp_time = problem.solve(
                instance,
                reward,
                n_scenarios_sol
            )
            ans[i] = of
        return ans
    
    def out_of_sample_stability(self, problem, sampler, instance, n_repertions, n_scenarios_sol, n_scenarios_out):
        ans = [0] * n_repertions
        for i in range(n_repertions):
            reward= sampler.sample_stoch(
                instance,
                n_scenarios=n_scenarios_sol
            )
            of, sol, comp_time = problem.solve(
                instance,
                reward,
                n_scenarios_sol
            )
            reward_out = sampler.sample_stoch(
                instance,
                n_scenarios=n_scenarios_out
            )
            profits = self.solve_second_stages(
                instance, sol,
                n_scenarios_out, reward_out,
                "profit"
            )
            ans[i]=np.mean(profits)
            
        return ans
