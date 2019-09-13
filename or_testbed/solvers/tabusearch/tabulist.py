# -*- coding:utf-8 -*-


"""
    OR-Testbed implementation of a Tabu List.

    This is a wrapper of Python's deque.
"""


from collections import deque


class TabuList:
    def __init__(self, maxlen=None):
        self._maxlen = maxlen
        self.list = deque(maxlen=maxlen)

    @property
    def maxlen(self):
        return self._maxlen

    def append(self, node):
        self.list.append(node)

    def index(self, node):
        try:
            return self.list.index(node)
        except ValueError:
            return -1

    def __contains__(self, node):
        return node in self.list
