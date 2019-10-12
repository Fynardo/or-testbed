# -*- coding:utf-8 -*-

"""
    TSP Resolution example:
        Simulated Annealing with initial solution calculated with GRASP
"""

from definition import SwapCitiesMove, tsp
from grasp import compute_grasp_solution
import or_testbed.solvers.simanneal as simanneal


# We need an initial solution, lets make a bad one
_, initial_sol = compute_grasp_solution()

tsp_moves = [SwapCitiesMove]
tsp_simanneal = simanneal.SimAnneal(tsp, initial_sol, tsp_moves, [1], 10, 0.1, 0.9, debug=True)
feasible, improved_sol = tsp_simanneal.solve()
print('Salesman will visit: {}'. format(improved_sol.cities))
