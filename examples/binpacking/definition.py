# -*- coding:utf-8 -*-

"""
    TSP Definition.

"""

import or_testbed.entities.solution as base_solution
import or_testbed.entities.instance as base_instance


class BPInstance(base_instance.Instance):
    def __init__(self, instance, data=None):
        super().__init__(instance, data)

    def is_feasible(self, in_solution):
        # TODO
        pass

    def calculate_objective(self, in_solution):
        # TODO
        pass


class BPSolution(base_solution.Solution):
    def __init__(self):
        super().__init__()
        # TODO


# TODO
# items = ...
# bins = ...
# bin_size = ...
# etc
#bp = BPInstance('binpacking_example', ...)
