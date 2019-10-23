# -*- coding:utf-8 -*-

import or_testbed.solvers.base.solver as base_solver


class BadSolver(base_solver.Solver):
    """
        This is a bad solver, it never will return a feasible solution.
    """
    def __init__(self):
        super().__init__(debug=False)
        self.solution = None
        self.feasible = False

    def optimize(self):
        return self.feasible, self.solution


class BadMultiStartSolver(base_solver.MultiStartSolver):
    def __init__(self):
        super().__init__(iters=10, inner_solver_factory=BadSolver.as_factory(), debug=False)


def test_bad_solver():
    bs = BadSolver()
    task = bs.solve()

    assert not task.is_feasible
    assert task.solution is None


def test_bad_ms_solver():
    bms = BadMultiStartSolver()
    task = bms.solve()

    assert not task.is_feasible
    assert task.solution is None

