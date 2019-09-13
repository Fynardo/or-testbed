# -*- coding:utf-8 -*-

import json


class Instance:
    """
        Instance objects hold information for concrete problem instances, like the input data.
        It also provides a basic loader from JSON coded input data.
    """

    def __init__(self, name, data=None):
        self._name = name
        self._data = data

    @property
    def name(self):
        """
        Basic getter for instance name

        :return: Instance name
        """
        return self._name

    @name.setter
    def name(self, in_name):
        """
            Basic setter for instance name

        :return: Instance name
        """
        self._name = in_name

    @property
    def data(self):
        """
            Basic getter for instance input data

        :return: Instance input data, its concrete structure is up to the developer.
        """
        return self._data

    @data.setter
    def data(self, in_data):
        """
            Basic setter for instance input data.

        :param in_data: Instance input data, its concrete structure is up to the developer.
        """
        self._data = in_data

    def from_file(self, path):
        """
            Basic data loader. It loads a json file and stores it in self.data attribute. For more complex loadings, overriding this method is recommended.

        :param path: Path of the JSON file
        """
        with open(path, 'r') as f:
            self.data = json.load(f)
