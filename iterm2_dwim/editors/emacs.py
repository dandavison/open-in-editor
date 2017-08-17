import re
import subprocess

from iterm2_dwim.logger import log

from iterm2_dwim.editors.base_editor import BaseEditor


class Emacs(BaseEditor):

    def visit_file(self, path, line):
        emacsclient = self.path_to_client
        path = re.sub('\.pyc$', '.py', path)

        cmd = [
            emacsclient,
            '--no-wait',
            '--eval', '(find-file "%s")' % path,
            '--eval', '(select-frame-set-input-focus (selected-frame))',
            '--eval', '(goto-line %d)' % line,
        ]
        log(' '.join(cmd))
        subprocess.check_call(cmd)
