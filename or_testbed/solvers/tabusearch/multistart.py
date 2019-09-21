# -*- coding:utf-8 -*-

import or_testbed.solvers.base.solver as base_solver


class MultiStartTabuSearch(base_solver.MultiStartSolver):
    """
        MultiStart version of Tabu Search.

        This is just an extension of base multistart solver. It works fine out of the box.
    """
    def __init__(self, iters, inner_tabusearch_factory, debug=True, log_file=None):
        super().__init__(iters, inner_tabusearch_factory, debug=debug, log_file=log_file)
        self.name = 'MultiStart Tabu Search'

