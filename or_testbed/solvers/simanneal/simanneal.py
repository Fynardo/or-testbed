# -*- coding:utf-8 -*-

import or_testbed.solvers.simanneal.exceptions
import or_testbed.solvers.base.solver as base_solver
import or_testbed.entities.neighborhood as neighborhood
import math
import random
import copy
from or_testbed.utils.logger import LogLevel


class SimAnneal(base_solver.Solver):
    """
        Simulated Annealing implementation.

        Based on Kirkpatricks work, this solver takes an initial solution and tries to improve it. It cannot create a new solution.

        Basically, simulated annealing uses an inspiration between the annealing process in metals and some topics in combinatorial optimization.
        The algorithm defines the space solution in terms of a neighborhood, and explores solutions modifying small parts of a solution.
        Then, the new solution is compared to the last one, if it is an improvement, new solution is accepted. If not, it's discarded.

        However, to avoid getting stuck in local optimal solutions, some worse solutions may be accepted (this is were the cooling parameter of the algorithm sets the probability of accepting a worse movement).

        In this algorithm, the developer needs to implement his own set of movements, everything else of the logic of the algorithm is already implemented.

        Check examples folder to see how to define and interact with simulated annealing.
    """
    def __init__(self, instance, initial_solution, available_movs, movs_weight, max_temp, min_temp, alpha, debug=True, log_file=None, log_level=LogLevel.ALL):
        super().__init__(debug, log_file, log_level)
        self.instance = instance
        self.initial_solution = initial_solution
        self.available_movs = available_movs
        self.movs_weight = movs_weight
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.alpha = alpha
        self.name = "Simulated Annealing"

    def _select_movement(self):
        """
            Selects a new movement of the defined set, taking into account the weight of each movement.

        :return: A movement to be made.
        """

        next_mov_class = random.choices(population=self.available_movs, cum_weights=self.movs_weight)[0]
        return next_mov_class

    def _make_move(self, next_mov, candidate, in_solution):
        """
            Executes a certain move, thus calculating a new neighbour solution.

        :param next_mov: A movement factory that the algorithm instantiates and executes.
        :param in_solution: The solution to make the move to and calculate a new neighbor.
        :return: The new neighbor solution.
        """
        new_sol = next_mov.apply(candidate, in_solution)
        new_sol.set_objective(new_sol.calculate_objective(self.instance))
        return new_sol

    def optimize(self):
        self.logger.log(LogLevel.INFO, 'Executing Simulated Annealing from {}ºC to {}ºC, {} rate', self.max_temp, self.min_temp, self.alpha)
        self.logger.log(LogLevel.INFO, 'Initial Solution Objective: {}', self.initial_solution.objective)

        best_sol = copy.deepcopy(self.initial_solution)
        current_sol = copy.deepcopy(self.initial_solution)
        current_temp = self.max_temp
        while current_temp >= self.min_temp:
            try:
                next_mov = self._select_movement()
                candidates = next_mov.make_neighborhood(current_sol, self.instance)
                candidate = neighborhood.select_candidate(neighborhood.strategy_factory('random'), candidates, current_sol, self.instance)
                fitness = candidate.fitness(current_sol, self.instance)
                if fitness > 0:
                    self._make_move(next_mov, candidate, current_sol)
                    self.logger.log(LogLevel.DEBUG, 'Improved solution by: {}. Move accepted', fitness)
                    if current_sol.compare_to(best_sol) > 0:
                        best_sol = copy.deepcopy(current_sol)
                elif fitness < 0:
                    # Sometimes bad solutions are accepted.
                    threshold = math.exp(fitness / current_temp)
                    if random.random() < threshold:
                        self._make_move(next_mov, candidate, current_sol)
                        self.logger.log(LogLevel.DEBUG, 'Worsened solution by: {}. Move Accepted', fitness)
                    else:
                        self.logger.log(LogLevel.DEBUG, 'Worsened solution by: {}. Move Rejected', fitness)

                current_temp *= self.alpha

            except or_testbed.solvers.simanneal.exceptions.MovementException:
                current_temp *= self.alpha
                continue

        feasible = best_sol.is_feasible(self.instance)
        return feasible, best_sol
