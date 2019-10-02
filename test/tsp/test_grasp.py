from .definition import *
from .instances import example_cities, example_initial_city
import or_testbed.solvers.grasp as base_grasp
import random
import pytest

tsp_instance = TSPInstance('tsp_example', example_cities, example_initial_city)
tsp_solution_factory = TSPSolution.factory(initial_city=tsp_instance.initial_city)


@pytest.fixture(autouse=True)
def run_around_tests():
    random.seed(12345)


def test_greedy_grasp():
    # Full greedy, bad solutions
    alpha = 0.0
    tsp_solver = base_grasp.GraspConstruct(tsp_instance, alpha=alpha, solution_factory=tsp_solution_factory, grasp_move=TSPGraspMove)
    task = tsp_solver.solve()
    assert task.is_feasible is True
    assert task.solution.objective == 34  # TODO no magic numbers pls


def test_random_grasp():
    # Full random, even worst solutions
    alpha = 1.0
    tsp_solver = base_grasp.GraspConstruct(tsp_instance, alpha=alpha, solution_factory=tsp_solution_factory, grasp_move=TSPGraspMove)
    task = tsp_solver.solve()
    assert task.is_feasible is True
    assert task.solution.objective == 43  # TODO no magic numbers pls


def test_grasp_multistart():
    random.seed(12345)

    tsp_grasp_factory = base_grasp.GraspConstruct.factory(instance=tsp_instance, alpha=0.3, solution_factory=tsp_solution_factory, grasp_move=TSPGraspMove, debug=False)
    tsp_multistart = base_grasp.MultiStartGraspConstruct(iters=25, inner_grasp_factory=tsp_grasp_factory)
    task = tsp_multistart.solve()

    assert task.is_feasible is True
    assert task.solution.objective == 17  # TODO no magic numbers pls
