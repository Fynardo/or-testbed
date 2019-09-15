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
    def __init__(self, name, data, initial_city):
        super().__init__(name, data)
        self.initial_city = initial_city


class TSPSolution(base_solution.Solution):
    def __init__(self, initial_city):
        super().__init__()
        self.initial_city = initial_city
        self.cities = [initial_city]

    def is_feasible(self, in_instance):
        """
            A solution is feasible if the salesman visits every city once and starts and finishes in the city marked as initial.
        """
        predicates = [
            len(self.cities) == len(in_instance.data.keys()),
            set(self.cities) == set(in_instance.data.keys()),
            self.cities[0] == in_instance.initial_city,
        ]
        return all(predicates)

    def calculate_objective(self, in_instance):
        """
            Objective value is the sum of the distances between cities (also taking into account returning to initial city).
        """
        return sum([in_instance.data[a][b] for a, b in zip(self.cities, self.cities[-1:] + self.cities[:-1])])


class SwapCitiesCandidate(base_candidate.Candidate):
    """
        This candidate is related to thw swapping cities move, basically it stores the cities to swap.
    """

    def __init__(self, city1, city2):
        self.city1 = city1
        self.city2 = city2

    def fitness(self, solution, instance):
        """
            Here fitness is calculated by making the actual move, then reverting it. Kind of a hack I know.
        """
        c1 = solution.cities.index(self.city1)
        c2 = solution.cities.index(self.city2)

        obj_before = solution.objective

        solution.cities[c1], solution.cities[c2] = solution.cities[c2], solution.cities[c1]
        obj_after = solution.calculate_objective(instance)
        solution.cities[c2], solution.cities[c1] = solution.cities[c1], solution.cities[c2]

        retval = obj_before - obj_after
        return retval


class SwapCitiesMove(base_move.Move):
    """
        Swapping cities is the most common move in TSP. It swaps the position of two cities in the sequence of cities to visit.
        The neighborhood is created by calculating the Cartesian Product of every city available except the initial one.
    """

    @staticmethod
    def make_neighborhood(solution, instance):
        # Cartesian Product
        swaps = itertools.combinations(instance.data.keys(), 2)
        # Filter to avoid moving initial city
        swaps = filter(lambda x: x[0] != instance.initial_city and x[1] != instance.initial_city, swaps)
        # Return list of candidates
        return [SwapCitiesCandidate(city1=s[0], city2=s[1]) for s in swaps]

    @staticmethod
    def apply(in_candidate, in_solution):
        first_city = in_solution.cities.index(in_candidate.city1)
        second_city = in_solution.cities.index(in_candidate.city2)

        in_solution.cities[first_city], in_solution.cities[second_city] = in_solution.cities[second_city], in_solution.cities[first_city]
        return in_solution


# Instance parameters
example_cities = {'A': {'B': 3, 'C': 5, 'D': 6, 'E': 2}, 'B': {'A': 3, 'C': 25, 'D': 10, 'E': 5}, 'C': {'A': 5, 'B': 25, 'D': 3, 'E': 4}, 'D': {'A': 6, 'B': 10, 'C': 3, 'E': 1},
                  'E': {'A': 2, 'B': 5, 'C': 4, 'D': 1}}
example_initial_city = 'A'
tsp = TSPInstance('tsp_example', example_cities, example_initial_city)
