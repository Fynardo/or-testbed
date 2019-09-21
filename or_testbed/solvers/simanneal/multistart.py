# -*- coding:utf-8 -*-

import or_testbed.solvers.base.solver as base_solver


class MultiStartSimAnneal(base_solver.MultiStartSolver):
    """
        MultiStart version of Simulated Annealing.

        This is just an extension of base multistart solver. It works fine out of the box.
    """
    def __init__(self, iters, inner_simanneal_factory, debug=True, log_file=None):
        super().__init__(iters, inner_simanneal_factory, debug=debug, log_file=log_file)
        self.name = 'MultiStart Simulated Annealing'

