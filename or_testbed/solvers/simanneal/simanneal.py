# -*- coding:utf-8 -*-

import or_testbed.solvers.simanneal.exceptions
import or_testbed.solvers.base.solver as base_solver
import math
import random
import copy


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
    def __init__(self, instance, initial_solution, available_movs, movs_weight, max_temp, min_temp, alpha, debug=True, log_file=None):
        super().__init__(debug, log_file)
        self.instance = instance
        self.initial_solution = initial_solution
        self.available_movs = available_movs
        self.movs_weight = movs_weight
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.alpha = alpha

    def _select_movement(self):
        """
            Selects a new movement of the defined set, taking into account the weight of each movement.

        :return: A movement to be made.
        """
        return random.choices(population=self.available_movs, cum_weights=self.movs_weight)[0]

    def _make_move(self, new_mov_factory, in_solution):
        """
            Executes a certain move, thus calculating a new neighbour solution.

        :param new_mov_factory: A movement factory that the algorithm instantiates and executes.
        :param in_solution: The solution to make the move to and calculate a new neighbor.
        :return: The new neighbor solution.
        """
        new_mov = new_mov_factory()
        neighbour = new_mov.execute(in_solution)
        return neighbour

    def optimize(self):
        self.logger.log('Executing Simulated Annealing from {}ºC to {}ºC, {} rate', self.max_temp, self.min_temp, self.alpha)
        self.logger.log('Initial Solution Objective: {}', self.initial_solution.objective)
        # TODO Copying a solution is very expensive in computational costs, it should be nice to define some backtracking approach. However the concrete approach
        # TODO  must be implemented by the developer.
        best_sol = copy.deepcopy(self.initial_solution)
        current_sol = copy.deepcopy(self.initial_solution)
        current_temp = self.max_temp
        while current_temp >= self.min_temp:
            try:
                next_mov = self._select_movement()
                new_sol = self._make_move(next_mov, copy.deepcopy(current_sol))
                new_sol.set_objective(new_sol.calculate_objective(self.instance))

                if new_sol.compare_to(best_sol) > 0:
                    best_sol = copy.deepcopy(new_sol)

                improvement = new_sol.compare_to(current_sol)
                if improvement > 0:
                    current_sol = new_sol
                    self.logger.log('Improved solution by: {}. Move accepted', improvement)
                elif improvement < 0:
                    # Sometimes bad solutions are accepted.
                    threshold = math.exp(improvement / current_temp)
                    if random.random() < threshold:
                        current_sol = new_sol
                        self.logger.log('Worsened solution by: {}. Move Accepted', improvement)
                    else:
                        self.logger.log('Worsened solution by: {}. Move Rejected', improvement)
                current_temp *= self.alpha
            except or_testbed.solvers.simanneal.exceptions.MovementException:
                current_temp *= self.alpha
                continue

        feasible = best_sol.is_feasible(self.instance)
        return feasible, best_sol
