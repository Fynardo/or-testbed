# -*- coding:utf-8 -*-

# TODO Adapt this to work also with *args


def make_factory_from(cls, **kwargs):
    """
        This function creates a factory from a class reference (``cls``) and its arguments. It is then used by the solvers which need to be able to instantiate any object like solutions or even other solvers.

    :param cls: Class Reference
    :param kwargs: Arguments for the class.
    :return: A function that, when executed, creates the object itself.
    """
    def inner_factory():
        return cls(**kwargs)
    return inner_factory
