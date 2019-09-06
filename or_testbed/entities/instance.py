# -*- coding:utf-8 -*-

import json


class Instance:
    """
        Instance objects hold information for concrete problem instances, like the input data.
        It also provides a basic loader from JSON coded input data.
    """

    def __init__(self, name, data=None):
        self.name = name
        self.data = data

    def set_data(self, in_data):
        """
            Basic setter for instance input data.

        :param in_data: Instance input data, its concrete structure is up to the developer.
        """
        self.data = in_data

    def get_data(self):
        """
        Basic getter for instance input data

        :return: Instance input data, its concrete structure is up to the developer.
        """

    def from_file(self, path):
        """
            Basic data loader. It loads a json file and stores it in self.data attribute. For more complex loadings, overriding this method is recommended.

        :param path: Path of the JSON file
        """
        with open(path, 'r') as f:
            self.data = json.load(f)
