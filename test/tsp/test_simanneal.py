from .definition import *
from .instances import example_cities, example_initial_city
import or_testbed.solvers.simanneal as base_simanneal
import or_testbed.solvers.grasp as base_grasp
import random
import pytest

tsp_instance = TSPInstance('tsp_example', example_cities, example_initial_city)
tsp_solution_factory = TSPSolution.as_factory(initial_city=tsp_instance.initial_city)


@pytest.fixture(autouse=True)
def run_around_tests():
    random.seed(12345)


def compute_grasp_solution():
    tsp_solver = base_grasp.GraspConstruct(tsp_instance, alpha=0.0, solution_factory=tsp_solution_factory, grasp_move=TSPGraspMove)
    task = tsp_solver.solve()
    return task.solution


def test_simanneal():
    initial_sol = compute_grasp_solution()

    tsp_moves = [SwapCitiesMove]
    tsp_simanneal = base_simanneal.SimAnneal(tsp_instance, initial_sol, tsp_moves, [1], 10, 0.1, 0.9, debug=True)
    task = tsp_simanneal.solve()
    assert task.is_feasible is True
    assert task.solution.objective == 17


def test_multistart_simanneal():
    initial_sol = compute_grasp_solution()

    tsp_moves = [SwapCitiesMove]
    simanneal_factory = base_simanneal.SimAnneal.as_factory(instance=tsp_instance, initial_solution=initial_sol, available_movs=tsp_moves, movs_weight=[1], max_temp=10, min_temp=1, alpha=0.9, debug=True)

    ms_simanneal = base_simanneal.MultiStartSimAnneal(10, simanneal_factory)
    task = ms_simanneal.solve()
    assert task.is_feasible is True
    assert task.solution.objective == 17
