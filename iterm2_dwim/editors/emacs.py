import subprocess

from iterm2_dwim.logger import log


class Editor(object):

    def edit_file(self, path, line):
        emacsclient = subprocess.check_output(['which', 'emacsclient']).strip()
        cmd = [
            emacsclient,
            '--no-wait',
            '--eval', '(find-file "%s")' % path,
            '--eval', '(select-frame-set-input-focus (selected-frame))',
            '--eval', '(goto-line %d)' % line,
        ]
        log(cmd)
        subprocess.check_call(cmd)
