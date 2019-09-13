# -*- coding:utf-8 -*-

import json
from abc import ABC, abstractmethod
from or_testbed.solvers.factory import make_factory_from


class Solution(ABC):
    """
        Solution objects store the proper solution structure of the problem being solved. Also, some logic is implemented, like checking if the solution
        is feasible and calculating the objective value (usually the cost function).

        Two solutions can be compared in terms of their objective values with compare_to method.
    """

    def __init__(self, objective=0):
        self.objective = objective

    @classmethod
    def factory(cls, **kwargs):
        return make_factory_from(cls, **kwargs)

    @abstractmethod
    def is_feasible(self, in_instance):
        """
            Checks if a solution is feasible or not, developer must override this method so it can fit the problem.

        :param in_instance: Problem instance with useful information.
        :return: True if solutino is feasible, False if it doesn't.
        """
        pass

    @abstractmethod
    def calculate_objective(self, in_instance):
        """
            Calculates the objective value of a solution (usually a cost function), developer must override this method so it can fit the problem.

        :param in_instance: Problem instance with useful information.
        :return: Objective value.
        """
        pass

    def set_objective(self, in_objective):
        """
            Simple setter for the objective value of the solution.

        :param in_objective: objective value.
        """
        self.objective = in_objective

    def get_objective(self):
        """
            Simple getter for the objective value of the solution.

        :return: Objective value
        """
        return self.objective

    def compare_to(self, in_solution, sense='MIN'):
        """
        Compares two solutions based on their objective values. This basic comparison supposes that the objective is a numeric value and a MINIMIZE type function.
        This method should be overriden if the objective is more complex than a single numeric value.

        :param in_solution: Another solution to compare with self one.
        :param sense: Indicates if we want to minimize (MIN) or maximize (MAX) the objective function.
        :return: Positive number if 'self' solution is better (less cost if MIN, greater cost if MAX). Negative number is 'self' solution is worse (greater cost if MIN, less cost if MAX). Zero if both solutions are equal (equal cost).
        """

        if sense == 'MIN':
            return in_solution.objective - self.objective
        elif sense == 'MAX':
            return self.objective - in_solution.objective

    def to_dict(self):
        """
            Tries to convert a solution to a dictionary. In case of complex solutions this method should be overriden.

        :return: The solution structure as a python dict.
        """
        return self.__dict__

    def to_json(self):
        """
            Tries to convert a solution to a JSON string. In case of complex solutions this method should be overriden.

        :return: The solution structure as a JSON string.
        """
        return json.dumps(self.to_dict())
