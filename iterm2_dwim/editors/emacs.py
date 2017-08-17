import re
import subprocess

from iterm2_dwim.logger import log


class Editor(object):

    def __init__(self, path, line):
        self.path = re.sub('\.pyc$', '.py', path)
        self.line = line

    def visit_file(self):
        emacsclient = subprocess.check_output(['which', 'emacsclient']).strip()
        cmd = [
            emacsclient,
            '--no-wait',
            '--eval', '(find-file "%s")' % self.path,
            '--eval', '(select-frame-set-input-focus (selected-frame))',
            '--eval', '(goto-line %d)' % self.line,
        ]
        log(' '.join(cmd))
        subprocess.check_call(cmd)
