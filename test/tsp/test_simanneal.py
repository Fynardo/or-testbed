from .definition import *
from .instances import example
import or_testbed.solvers.simanneal as base_simanneal
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


def test_simanneal():
    _, initial_sol = compute_grasp_solution()

    tsp_moves = [SwapCitiesMove]
    tsp_simanneal = base_simanneal.SimAnneal(tsp_instance, initial_sol, tsp_moves, [1], 10, 0.1, 0.9, debug=True)
    feasible, improved_sol = tsp_simanneal.solve()
    assert feasible is True
    assert improved_sol.objective == 17


def test_multistart_simanneal():
    _, initial_sol = compute_grasp_solution()

    tsp_moves = [SwapCitiesMove]
    simanneal_factory = base_simanneal.SimAnneal.factory(instance=tsp_instance, initial_solution=initial_sol, available_movs=tsp_moves, movs_weight=[1], max_temp=10, min_temp=1, alpha=0.9, debug=True)

    ms_simanneal = base_simanneal.MultiStartSimAnneal(10, simanneal_factory)
    feasible, solution = ms_simanneal.solve()
    assert feasible is True
    assert solution.objective == 17
