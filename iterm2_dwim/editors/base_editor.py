import re


class BaseEditor(object):

    def __init__(self, path_to_client):
        self.path_to_client = path_to_client
