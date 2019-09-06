# -*- coding:utf-8 -*-

import or_testbed.solvers.base.solver as base_solver
from abc import abstractmethod
import random


class MultiStartGraspConstruct(base_solver.MultiStartSolver):
    """
        MultiStart version of GRASP constructive.

        This is just an extension of base multistart solver. It works fine out of the box.
    """

    def __init__(self, iters, inner_grasp_factory, debug=True, log_file=None):
        super().__init__(iters, inner_grasp_factory, debug=debug, log_file=log_file)
        self.name = 'MultiStartGRASP'


class GraspConstruct(base_solver.Solver):
    """
        GRASP constructive version.

        This class implements GRASP with parameter alpha, which handles the randomness related to the space exploration.

        To construct a solution, what it does is basically 4 steps:

        1. Defines candidates to add to the solution.
        2. Applies a greedy function to each candidate to calculate the incurring cost of adding that candidate to the solution.
        3. Ranks candidates according to this cost.
        4. Filters candidates depending on their costs, depending on alpha parameter, this creates the Restricted Candidates List (RCL)
        5. Adds one random candidate to the solution.

        The core of the algorithm is implemented in this class, see ``optimize`` method.
        The developer needs to override the methods that handle the candidates and the greedy function, as that is what is needed to adapt GRASP to any problem.

        Check examples folder to see how to define and interact with GRASP.
    """

    def __init__(self, instance, solution_factory, alpha, debug=True, log_file=None):
        super().__init__(debug, log_file)
        self.instance = instance
        self.alpha = alpha
        self.solution_factory = solution_factory
        self.solution = self.solution_factory()

    def _filter_candidate_list(self, candidates, costs):
        """
            This method takes a candidates list and their related costs based on a greedy function, then it filters those candidates whose associated cost fits the following expression:

            ``c_min <= c(e) <= c_min + alpha*(c_max - c_min)``

            Where:
                * ``c(e)`` is the cost of candidate ``e``
                * ``c_min`` is the minimum cost of all candidates
                * ``c_max`` is the maximum cost of all candidates

            This means that when parameter alpha is 0, a pure greedy approach is followed, only taking into account those candidates with minimum cost. On the other hand, if alpha is 1, then a pure random approach is followed, taking into account all candidates. Optimal value usually is somewhere in between.

        :param candidates: List of candidates to filter.
        :param costs: List of costs associated with each candidate.
        :return: Filtered list of candidates depending of their cost.
        """

        c_min = min(costs)
        c_max = max(costs)
        return [candidates[i] for i, c in enumerate(costs) if c_min <= c <= c_min + self.alpha * (c_max - c_min)]

    def _make_rcl(self):
        """
            This method creates the Restricted Candidates List (RCL). It gets all the candidates, calculate thier costs and filter them according to parameter alpha.

        :return: Calculated RCL
        """
        candidates_list = self._make_candidates_list()
        cost_list = list(map(self._greedy_function, candidates_list))
        rcl = self._filter_candidate_list(candidates_list, cost_list)
        return rcl

    def _select_candidate(self, rcl):
        """
            Selects next candidate to add to the solution from the RCL. It just selects a random candidate by default.

        :param rcl: Restricted Candidates List
        :return: Selected candidate from RCL
        """
        return random.choice(rcl)

    def optimize(self):
        self.logger.log('Executing GRASP Construct on instance {} with alpha {}.', self.instance.name, self.alpha)
        self._initialize_solution()

        while self._are_candidates_left():
            rcl = self._make_rcl()
            candidate = self._select_candidate(rcl)
            self._add_candidate(candidate)
            self.solution.set_objective(self.solution.calculate_objective(self.instance))

        feasible = self.solution.is_feasible(self.instance)
        return feasible, self.solution

    def _initialize_solution(self):
        pass

    @abstractmethod
    def _greedy_function(self, candidate):
        """
            This method calculates greedy function value of a candidate. Developer must override this method.

        :param candidate: A candidate to calculate greedy function.
        :return: Greedy function cost of the candidate.
        """
        pass

    @abstractmethod
    def _are_candidates_left(self):
        """
            This method checks if there are more candidates remaining that need to be added to the solution. Developer must override this method.

        :return: True if there are candidates left, False otherwise
        """
        return False

    @abstractmethod
    def _make_candidates_list(self):
        """
            This method calculates the list of remaining candidates that need to be added to the solution. Developer must override this method.

        :return: A remaining candidates list.
        """
        pass

    @abstractmethod
    def _add_candidate(self, candidate):
        """
            This method adds a candidate to the solution structure. Developer must override this method.

        :param candidate: Selected candidate to be added to the solution
        """
        pass
