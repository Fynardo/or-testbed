# -*- coding:utf-8 -*-

# TODO Adapt this to work also with *args


def make_factory_from(cls, *args, **kwargs):
    """
        This function creates a factory from a class reference (``cls``) and its arguments. It is then used by the solvers which need to be able to instantiate any object like solutions or even other solvers.

    :param cls: Class Reference
    :param args: Argument list with class parameters
    :param kwargs: Argument dictionary with class parameters
    :return: A function that, when executed, creates the object itself.
    """
    def inner_factory():
        return cls(*args, **kwargs)
    return inner_factory
