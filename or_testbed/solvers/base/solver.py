# -*- coding:utf-8 -*-

import time
from abc import abstractmethod, ABC
from or_testbed.utils.logger import Logger, LogLevel
from or_testbed.solvers.factory import make_factory_from
import copy


class Solver(ABC):
    """
        Base solver class.

        Every solver in OR-Testbed extends this class. What is important is that it implements the ``solve`` method, which actually runs the solver.

        To add new solvers, ``optimize`` method must be overriden, there's where all the solver logic lives.

    """
    def __init__(self, debug=True, log_file=None, log_level=LogLevel.ALL):
        self.logger = Logger(debug=debug, log_file=log_file, log_level=log_level)
        self.name = "BaseSolver"

    def solve(self):
        """
            This method runs the solver, measures execution time and logs the result.

        :return: A tuple including a boolean value indicating if the solution is feasible and the solution itself.
        """
        start = time.time()
        feasible, solution = self.optimize()
        end = time.time() - start
        self.logger.log(LogLevel.RESULT, '{solver} Done! Finished in {time} seconds. Objective: {obj}. Feasible: {feasible}\n', solver=self.name,  time=round(end, 8), obj=solution.objective, feasible=feasible)
        return feasible, solution

    @classmethod
    def factory(cls, **kwargs):
        """
            This method returns a factory able to instantiate objects whenever needed

        :param kwargs: Arguments dict for the class
        :return: A factory function
        """
        return make_factory_from(cls, **kwargs)

    @abstractmethod
    def optimize(self):
        pass


class MultiStartSolver:
    """
        Base multistart solver class.

        Every multistart solver in OR-Testbed extend this class, but just for commodity purposes, since this class works just fine by itself.

        It just executes a solver any given amount of times (``iters`` parameter) and returns the best result achieved.

    """
    def __init__(self, iters, inner_solver_factory, debug=True, log_file=None, log_level=LogLevel.ALL):
        self.logger = Logger(debug=debug, log_file=log_file, log_level=log_level)
        self.name = 'IteratedBase'
        self.iters = iters
        self.inner_solver_factory = inner_solver_factory
        self.best_sol = {'feasible': False, 'solution': None}

    def solve(self):
        self.logger.log(LogLevel.INFO, 'Executing {} {} times.', self.name, self.iters)
        start = time.time()
        for current_iter in range(self.iters):
            inner_solver = self.inner_solver_factory()
            feasible, current_solution = inner_solver.solve()

            if self.best_sol['solution'] is None or current_solution.compare_to(self.best_sol['solution']) > 0:
                self.best_sol['feasible'] = feasible
                self.best_sol['solution'] = copy.deepcopy(current_solution)
                self.logger.log(LogLevel.DEBUG, 'Iter {}. Solution Improved. New obj: {}.', current_iter, current_solution.objective)

        end = time.time() - start
        self.logger.log(LogLevel.RESULT, '{solver} Done! Finished in {time} seconds. Objective: {obj}. Feasible: {feasible}\n', solver=self.name, time=round(end, 8), obj=self.best_sol['solution'].objective, feasible=self.best_sol['feasible'])
        return self.best_sol['feasible'], self.best_sol['solution']
