# -*- coding: utf8 -*-

# TODO Add timestamp to log entries.


from enum import Enum


class LogLevel(Enum):
    NONE = 0
    RESULT = 1
    INFO = 2
    DEBUG = 3
    ALL = 4

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented


class Message:
    def __init__(self, strf, *args, **kwargs):
        self.strf = strf
        self.args = args
        self.kwargs = kwargs

    def get_args(self):
        return self.args

    def get_kwargs(self):
        return self.kwargs

    def mkstring(self):
        if self.args:
            retval = self.strf.format(*self.args)
        elif self.kwargs:
            retval = self.strf.format(**self.kwargs)
        else:
            retval = self.strf
        return retval


class Logger:
    """
        OR-Testbed logging utility.

        It lets the developer to create messages that can be printed to standard output (console) of stored into a file.
    """
    def __init__(self, debug=True, log_file=None, log_level=LogLevel.ALL):
        self.debug = debug
        self.log_file = log_file
        self.log_level = log_level

    def log(self, level, strf, *args, **kwargs):
        """
            This method creates a message and, depending on attributes ``debug`` and ``log_file`` it prints or stores them (or both).

            It takes a string formated in Python *new style* and some arguments to create the message.
            For example:

            * ``strf='Hello, {}'`` and ``*args = ['World']`` will make the message ``'Hello, World'``.

            * ``strf='Hello, {name}'`` and ``**kwargs = {'name': 'James'}`` will make the message ``'Hello, James'``.

        :param level: Level of message.
        :param strf: String with Python *new style* format.
        :param args: Arguments to be referenced in positional format.
        :param kwargs: Arguments to be referenced in key-value format.
        """
        msg = Message(strf, *args, **kwargs)
        if self.log_level >= level:
            if self.debug:
                print(msg.mkstring())
            if self.log_file:
                with open(self.log_file, 'a') as f:
                    f.write(msg.mkstring() + '\n')
