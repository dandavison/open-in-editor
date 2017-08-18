class BaseEditor(object):
    """
    Abstract base class for editors.
    """

    def __init__(self, executable):
        self.executable = executable

    def visit_file(self, path, line):
        raise NotImplementedError()
