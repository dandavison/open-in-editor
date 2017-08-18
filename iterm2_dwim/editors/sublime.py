import subprocess

from iterm2_dwim.editors.base import BaseEditor
from iterm2_dwim.logger import log


class Sublime(BaseEditor):

    def visit_file(self, path, line):
        cmd = [
            self.executable,
            '%s:%s' % (path, line)
        ]
        log(' '.join(cmd))
        subprocess.check_call(cmd)
