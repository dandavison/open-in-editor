#!/usr/bin/env python
import sys
from typing import Optional
from urllib.parse import urlparse

from open_in_editor import editors
from open_in_editor import settings
from open_in_editor.logger import log


def parse_url(url) -> (str, Optional[int], Optional[int]):
    """
    Parse a file-like URL into path, line, and column.

    >>> parse_url("file:///a/b/myfile.txt")
    ('/a/b/myfile.txt', None, None)

    >>> parse_url("file-line-column:///a/b/myfile.txt")
    ('/a/b/myfile.txt', None, None)

    >>> parse_url("file:///a/b/myfile.txt:7")
    ('/a/b/myfile.txt', 7, None)

    >>> parse_url("file:///a/b/myfile.txt:7:77")
    ('/a/b/myfile.txt', 7, 77)

    >>> parse_url("file://localhost/a/b/myfile.txt:7:77")
    ('/a/b/myfile.txt', 7, 77)
    """
    path, _, line_and_column = urlparse(url).path.partition(":")
    line, _, column = line_and_column.partition(":")
    try:
        line = int(line)
    except ValueError:
        line = None
    try:
        column = int(column)
    except ValueError:
        column = None
    return path, line, column


def main():
    if settings.sublime:
        Editor = editors.Sublime(settings.sublime)
    elif settings.emacsclient:
        Editor = editors.Emacs(settings.emacsclient)
    elif settings.vscode:
        Editor = editors.VSCode(settings.vscode)
    elif settings.pycharm:
        Editor = editors.PyCharm(settings.pycharm)
    else:
        log("ERROR: No editor specified in settings.py")
        sys.exit(1)

    try:
        url, = sys.argv[1:]

        path, line, _ = parse_url(url)

        log(f"path={path} line={line}")

        Editor.visit_file(path, line or 1)
    except Exception as exc:
        from traceback import format_exc
        log(format_exc())
