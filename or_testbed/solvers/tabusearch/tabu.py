# -*- coding:utf-8 -*-

import or_testbed.solvers.base.solver as base_solver
from .tabulist import TabuList
import or_testbed.entities.neighborhood as neighborhood
from or_testbed.utils.logger import LogLevel
import copy
import random


class TabuSearch(base_solver.Solver):
    """
        Tabu Search (TS) implementation.

        Based on Glover work, this solver takes an initial solution and tries to improve it. It cannot create a new solution.

        Basically, tabu search explores the solution space the same way as other trajectory solvers. It  defines the space solution in terms of a neighborhood,
        and explores modifying small parts of a solution.

        The main feature of TS is that, in order to avoid getting stuck, it uses a list where recent neighbors are stored, so it does not run in circles over the same
        solutions over and over again.

        When a candidate is accepted, it is added to the tabu list, sometimes, if no good solution is found, a bad solution can be taken to continue the exploration.
        When the tabu list is full, elements get discarded in favor of new ones.

        Check examples folder to see how to define and interact with tabu search.
    """
    def __init__(self, instance, initial_solution, available_movs, movs_weight, tabulen=10, iters=10, candidate_selection='first', debug=True, log_file=None, log_level=LogLevel.ALL):
        super().__init__(debug, log_file, log_level=log_level)
        self.instance = instance
        self.initial_sol = initial_solution
        self.available_movs = available_movs
        self.movs_weight = movs_weight
        self.tabulen = tabulen
        self.tabu = TabuList(maxlen=tabulen)
        self.iters = iters
        self.candidate_selection = candidate_selection
        self.candidates_strategy = neighborhood.strategy_factory(self.candidate_selection)
        self.name = "Tabu Search"

    def optimize(self):
        self.logger.log(LogLevel.INFO, 'Executing {}, {} iterations. Candidate selection strategy: {}', self.name, self.iters, self.candidate_selection)
        self.logger.log(LogLevel.INFO, 'Initial Solution Objective: {}', self.initial_sol.objective)

        best_sol = copy.deepcopy(self.initial_sol)
        current_sol = copy.deepcopy(self.initial_sol)

        for iter in range(self.iters):
            next_mov_class = random.choices(population=self.available_movs, cum_weights=self.movs_weight)[0]
            candidates = next_mov_class.make_neighborhood(current_sol, self.instance)
            cost, candidate = neighborhood.select_candidate(self.candidates_strategy, candidates, current_sol, self.instance)
            if candidate not in self.tabu:
                self.logger.log(LogLevel.DEBUG, 'Iter {}. Candidate: {} ({})', iter, candidate, cost)
                self.tabu.append(candidate)
                current_sol = next_mov_class.apply(candidate, current_sol)
                current_sol.set_objective(current_sol.calculate_objective(self.instance))

                if current_sol.compare_to(best_sol) > 0:
                    best_sol = copy.deepcopy(current_sol)

        feasible = best_sol.is_feasible(self.instance)
        return feasible, best_sol
