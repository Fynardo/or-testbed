from .definition import *
from .instances import example
import or_testbed.solvers.tabusearch as base_tabu
import or_testbed.solvers.grasp as base_grasp
import random
import pytest

tsp_instance = TSPInstance('tsp_example', example)
tsp_solution_factory = TSPSolution.factory(initial_city='A')


@pytest.fixture(autouse=True)
def run_around_tests():
    random.seed(12345)


def compute_grasp_solution():
    tsp_solver = base_grasp.GraspConstruct(tsp_instance, alpha=0.0, solution_factory=tsp_solution_factory, grasp_move=TSPGraspMove)
    feasible, solution = tsp_solver.solve()
    return feasible, solution


def test_tabu():
    _, initial_sol = compute_grasp_solution()

    tsp_moves = [SwapCitiesMove]
    tsp_tabu = base_tabu.TabuSearch(tsp_instance, initial_sol, tsp_moves, [1], 10, 10)
    feasible, improved_sol = tsp_tabu.solve()
    assert feasible is True
    assert improved_sol.objective == 17


def test_multistart_tabu():
    _, initial_sol = compute_grasp_solution()

    tsp_moves = [SwapCitiesMove]
    tabu_factory = base_tabu.TabuSearch.factory(instance=tsp_instance, initial_solution=initial_sol, available_movs=tsp_moves, movs_weight=[1], iters=10, tabulen=1)

    ms_tabu = base_tabu.MultiStartTabuSearch(10, tabu_factory)
    feasible, solution = ms_tabu.solve()
    assert feasible is True
    assert solution.objective == 17
