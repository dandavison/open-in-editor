import subprocess

from iterm2_dwim.editors.base import BaseEditor
from iterm2_dwim.logger import log


class Emacs(BaseEditor):

    def visit_file(self, path, line):
        cmd = [
            self.executable,
            '--no-wait',
            '--eval', '(find-file "%s")' % path,
            '--eval', '(select-frame-set-input-focus (selected-frame))',
            '--eval', '(goto-line %d)' % line,
        ]
        log(' '.join(cmd))
        subprocess.check_call(cmd)
