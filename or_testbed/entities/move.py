# -*- coding:utf-8 -*-

from abc import ABC, abstractmethod


class Move(ABC):
    @staticmethod
    @abstractmethod
    def make_neighborhood(solution, instance):
        pass

    @staticmethod
    @abstractmethod
    def apply(in_candidate, in_solution):
        pass
