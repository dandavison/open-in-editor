import subprocess

from open_in_editor.editors.base import BaseEditor
from open_in_editor.logger import log


class VSCode(BaseEditor):
    def visit_file(self, path, line):
        cmd = [self.executable, "-g", "%s:%s" % (path, line)]
        log(" ".join(cmd))
        subprocess.check_call(cmd)
