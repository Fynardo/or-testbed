# -*- coding:utf-8 -*-

"""
    TSP Definition.

"""

import or_testbed.entities.solution as base_solution
import or_testbed.entities.instance as base_instance


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


cities = {'A': {'B': 3, 'C': 5, 'D': 6, 'E': 2}, 'B': {'A': 3, 'C': 25, 'D': 10, 'E': 5}, 'C': {'A': 5, 'B': 25, 'D': 3, 'E': 4}, 'D': {'A': 6, 'B': 10, 'C': 3, 'E': 1}, 'E': {'A': 2, 'B': 5, 'C': 4, 'D': 1}}
tsp = TSPInstance('tsp_example', cities)
