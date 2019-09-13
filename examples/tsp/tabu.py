# -*- coding:utf-8 -*-

"""
    TSP Resolution example:
        Tabu Search with initial solution calculated with GRASP
"""

from definition import TSPInstance, TSPSolution, SwapCitiesCandidate, SwapCitiesMove, tsp
from grasp import compute_grasp_solution
import or_testbed.solvers.tabusearch as tabusearch


# We need an initial solution, lets make a bad one
_, initial_sol = compute_grasp_solution()

tsp_moves = [SwapCitiesMove]
tsp_tabu = tabusearch.TabuSearch(tsp, initial_sol, tsp_moves, [1], candidate_selection='best')
feasible, improved_sol = tsp_tabu.solve()
