# -*- coding:utf-8 -*-

"""
    TSP Definition.

"""

import or_testbed.entities.solution as base_solution
import or_testbed.entities.instance as base_instance
import or_testbed.entities.candidate as base_candidate
import or_testbed.entities.move as base_move
import itertools


class TSPInstance(base_instance.Instance):
    def __init__(self, name, data=None):
        super().__init__(name, data)


class TSPSolution(base_solution.Solution):
    def __init__(self, initial_city):
        super().__init__()
        self.initial_city = initial_city
        self.cities = [initial_city]

    def is_feasible(self, in_instance):
        return set(self.cities) == set(in_instance.data.keys())

    def calculate_objective(self, in_instance):
        return sum([in_instance.data[a][b] for a,b in zip(self.cities, self.cities[-1:] + self.cities[:-1])])


class SwapCitiesCandidate(base_candidate.Candidate):
    def __init__(self, city1, city2):
        self.city1 = city1
        self.city2 = city2

    def fitness(self, solution, instance):
        c1 = solution.cities.index(self.city1)
        c2 = solution.cities.index(self.city2)

        obj_before = solution.objective

        solution.cities[c1], solution.cities[c2] = solution.cities[c2], solution.cities[c1]
        obj_after = solution.calculate_objective(instance)
        solution.cities[c2], solution.cities[c1] = solution.cities[c1], solution.cities[c2]

        retval = obj_before - obj_after
        return retval


class SwapCitiesMove(base_move.Move):
    @staticmethod
    def make_neighborhood(solution, instance):
        swaps = itertools.combinations(instance.data.keys(), 2)
        return [SwapCitiesCandidate(city1=s[0], city2=s[1]) for s in swaps]

    @staticmethod
    def apply(in_candidate, in_solution):
        first_city = in_solution.cities.index(in_candidate.city1)
        second_city = in_solution.cities.index(in_candidate.city2)

        in_solution.cities[first_city], in_solution.cities[second_city] = in_solution.cities[second_city], in_solution.cities[first_city]
        return in_solution


cities = {'A': {'B': 3, 'C': 5, 'D': 6, 'E': 2}, 'B': {'A': 3, 'C': 25, 'D': 10, 'E': 5}, 'C': {'A': 5, 'B': 25, 'D': 3, 'E': 4}, 'D': {'A': 6, 'B': 10, 'C': 3, 'E': 1}, 'E': {'A': 2, 'B': 5, 'C': 4, 'D': 1}}
tsp = TSPInstance('tsp_example', cities)
