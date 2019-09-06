# -*- coding:utf-8 -*


class SimAnnealBaseException(Exception):
    pass


class MovementException(SimAnnealBaseException):
    def __init__(self, message, ex_type):
        self.message = message
        self.ex_type = ex_type
