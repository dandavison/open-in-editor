import subprocess

from open_in_editor.editors.base import BaseEditor
from open_in_editor.logger import log


class PyCharm(BaseEditor):
    def visit_file(self, path, line):
        cmd = [self.executable, "--line", str(line), path]
        log(" ".join(cmd))
        subprocess.check_call([s.encode("utf-8") for s in cmd])
