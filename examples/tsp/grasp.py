# -*- coding:utf-8 -*-

"""
    TSP Resolution example:
        GRASP Algorithm
"""

from definition import TSPInstance, TSPSolution, tsp
import or_testbed.solvers.grasp as base_grasp
from or_testbed.solvers.factory import make_factory_from


class TSPGrasp(base_grasp.GraspConstruct):
    def __init__(self, instance, solution_factory, alpha, debug=True, log_file=None):
        super().__init__(instance, solution_factory, alpha, debug, log_file)
        self.visited = set()
        self.left = set(self.instance.data.keys())
        self.last_visited = self.solution.initial_city

    def _initialize_solution(self):
        self.visited.add(self.solution.initial_city)
        self.left.remove(self.solution.initial_city)

    def _greedy_function(self, candidate):
        return self.instance.data[self.last_visited][candidate]

    def _are_candidates_left(self):
        return True if self.left else False

    def _add_candidate(self, candidate):
        self.solution.cities.append(candidate)
        self.visited.add(candidate)
        self.last_visited = candidate
        self.left.remove(candidate)

    def _make_candidates_list(self):
        return [c for c in self.instance.data[self.last_visited].keys() if c not in self.visited]


if __name__ == '__main__':
    tsp_solution_factory = make_factory_from(TSPSolution, initial_city='A')
    tsp_solver = TSPGrasp(tsp, alpha=0.0, solution_factory=tsp_solution_factory)
    feasible, solution = tsp_solver.solve()
    print('Salesman will visit: {}'.format(solution.cities))
    print('Total cost: {}'.format(solution.get_objective()))
