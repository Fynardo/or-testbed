# -*- coding:utf-8 -*-

"""
    TSP Resolution example:
        GRASP Algorithm
"""

from definition import TSPInstance, TSPSolution, tsp
import or_testbed.solvers.grasp as base_grasp
import or_testbed.entities.candidate as base_candidate
import or_testbed.entities.move as base_move


class TSPGraspCandidate(base_candidate.Candidate):
    def __init__(self, city):
        self.city = city

    def fitness(self, solution, instance):
        last_visited = solution.cities[-1]
        return instance.data[last_visited][self.city]


class TSPGraspMove(base_move.Move):
    """
        When constructing a solution, GRASP only has one move, that is to add candidates to the solution.
    """
    @staticmethod
    def make_neighborhood(solution, instance):
        return [TSPGraspCandidate(city=c) for c in instance.data[solution.cities[-1]].keys() if c not in solution.cities]

    @staticmethod
    def apply(in_candidate, in_solution):
        in_solution.cities.append(in_candidate.city)
        return in_solution


def compute_grasp_solution():
    tsp_solution_factory = TSPSolution.factory(tsp.initial_city)
    tsp_solver = base_grasp.GraspConstruct(tsp, alpha=0.0, solution_factory=tsp_solution_factory, grasp_move=TSPGraspMove)
    feasible, solution = tsp_solver.solve()
    return feasible, solution


if __name__ == '__main__':
    feasible, solution = compute_grasp_solution()
    print('Salesman will visit: {}'.format(solution.cities))
