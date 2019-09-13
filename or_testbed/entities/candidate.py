# -*- coding:utf-8 -*-


"""
    Candidate implementation for OR-Testbed.

"""

from abc import ABC, abstractmethod


class Candidate(ABC):
    """
        in OR-Testbed a candidate is used to model potential moves in trajectory solvers, such as simulated annealing or tabu search.
        Concrete attributes of a candidate depend on the problem being solved.
    """

    @abstractmethod
    def fitness(self, solution, instance):
        """
            Fitness function of a candidate. Usually this means the improvement of selecting this candidate to the actual solution.

        :param solution: Actual solution that the candidate will modify.
        :param instance: Instance being solved, may be needed to check special requirements or data.
        :return: Fitness of the candidate, usually a numeric value.
        """
        pass

    def __eq__(self, other):
        """
            Determine if two candidates are equal based on values of their attributes. All attributes must be hashable, otherwise comparison using __dict__ won't be possible.
            When dealing with complex candidates, developer should override this method.

        :param other: Other NodeList object to compare to.
        :return: True if self and other are considered equal, False otherwise.
        """
        retval = False
        if isinstance(other, Candidate):
            self_attrs = self.__dict__
            node_attrs = other.__dict__
            if self_attrs.keys() == node_attrs.keys():
                retval = all([self_attrs[k] == node_attrs[k] for k in self_attrs.keys()])
        return retval

    def __str__(self):
        return str(self.__dict__)