import subprocess

from iterm2_dwim.logger import log

from iterm2_dwim.editors.base_editor import BaseEditor
from iterm2_dwim.settings import path_to_subl


class Sublime(BaseEditor):

    def __init__(self, path, line):
        super(Sublime, self).__init__(path, line)

    def visit_file(self):
        subl = path_to_subl
        cmd = [
            subl,
            '%s:%s' % (self.path, self.line)
        ]
        log(cmd)
        subprocess.check_call(cmd)
