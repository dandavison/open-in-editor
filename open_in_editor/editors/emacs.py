import subprocess

from open_in_editor.editors.base import BaseEditor
from open_in_editor.logger import log


class Emacs(BaseEditor):
    def visit_file(self, path, line):
        cmd = [
            self.executable,
            "--no-wait",
            "--eval",
            '(find-file "%s")' % path,
            "--eval",
            "(goto-line %d)" % line,
            "--eval",
            "(recenter-top-bottom)",
            "--eval",
            "(select-frame-set-input-focus (selected-frame))",
            "--eval",
            "(when (functionp 'pulse-momentary-highlight-one-line)"
            " (let ((pulse-delay 0.05)) (pulse-momentary-highlight-one-line (point) 'highlight)))",
        ]
        log(" ".join(cmd))
        subprocess.check_call(cmd)
