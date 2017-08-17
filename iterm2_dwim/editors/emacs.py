import subprocess

from iterm2_dwim.logger import log

from iterm2_dwim.editors.base_editor import BaseEditor
from iterm2_dwim.settings import path_to_emacsclient


class Emacs(BaseEditor):

    def __init__(self, path, line):
        super(Emacs, self).__init__(path, line)

    def visit_file(self):
        emacsclient = path_to_emacsclient
        cmd = [
            emacsclient,
            '--no-wait',
            '--eval', '(find-file "%s")' % self.path,
            '--eval', '(select-frame-set-input-focus (selected-frame))',
            '--eval', '(goto-line %d)' % self.line,
        ]
        log(cmd)
        subprocess.check_call(cmd)
