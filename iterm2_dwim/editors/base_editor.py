import re


class BaseEditor(object):

    def __init__(self, path, line):
        self.path = re.sub('\.pyc$', '.py', path)
        self.line = line
