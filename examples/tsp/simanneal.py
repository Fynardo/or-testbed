# -*- coding:utf-8 -*-

"""
    TSP Resolution example:
        Simulated Annealing with initial solution calculated with GRASP
"""

from definition import TSPInstance, TSPSolution, tsp
from grasp import TSPGrasp
import or_testbed.solvers.simanneal as simanneal
import or_testbed.solvers.base.move as base_move
from or_testbed.solvers.factory import make_factory_from
import random


class SwapCitiesMove(base_move.Move):
    def execute(self, in_solution):
        first_city = random.randrange(len(in_solution.cities))
        second_city = random.randrange(len(in_solution.cities))

        in_solution.cities[first_city], in_solution.cities[second_city] = in_solution.cities[second_city], in_solution.cities[first_city]
        return in_solution


tsp_moves = make_factory_from(SwapCitiesMove)

# We need an initial solution, lets make a bad one
tsp_solution_factory = make_factory_from(TSPSolution, initial_city='A')
tsp_solver = TSPGrasp(tsp, alpha=0.0, solution_factory=tsp_solution_factory, debug=False)
_, initial_solution = tsp_solver.solve()

tsp_simanneal = simanneal.SimAnneal(tsp, initial_solution, [tsp_moves], [1], 10, 1, 0.9, debug=True)
feasible, improved_sol = tsp_simanneal.solve()

# Iterated Simulated Annealing
tsp_simanneal_factory = make_factory_from(simanneal.SimAnneal, instance=tsp, initial_solution=initial_solution, available_movs=[tsp_moves], movs_weight=[1], max_temp=10, min_temp=1, alpha=0.9, debug=False)
tsp_iterated_simanneal = simanneal.MultiStartSimAnneal(2, tsp_simanneal_factory, debug=True)
feasible, another_improved_sol = tsp_iterated_simanneal.solve()
