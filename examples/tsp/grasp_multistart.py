# -*- coding:utf-8 -*-

"""
    TSP Resolution example:
        GRASP Algorithm with a multistart approach
"""

from definition import TSPInstance, TSPSolution, tsp
from grasp import TSPGraspMove
import or_testbed.solvers.grasp as base_grasp



if __name__ == '__main__':
    tsp_solution_factory = TSPSolution.factory(initial_city='A')
    tsp_grasp_factory = base_grasp.GraspConstruct.factory(instance=tsp, alpha=0.3, solution_factory=tsp_solution_factory, grasp_move=TSPGraspMove, debug=False)

    tsp_multistart = base_grasp.MultiStartGraspConstruct(iters=25, inner_grasp_factory=tsp_grasp_factory)
    feasible, ms_solution = tsp_multistart.solve()
    print('Salesman will visit: {}'.format(ms_solution.cities))
    print('Total cost: {}'.format(ms_solution.get_objective()))
