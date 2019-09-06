# -*- coding:utf-8 -*-

from abc import abstractmethod


class Move:
    @abstractmethod
    def execute(self, in_solution):
        pass
