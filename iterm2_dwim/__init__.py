#!/usr/bin/env python
from contextlib import contextmanager
import os
import re
import subprocess
import sys

from iterm2_dwim.editors import emacs
from iterm2_dwim.logger import log


Editor = emacs.Editor


def notify(message):
    subprocess.check_call([
        '/usr/local/bin/terminal-notifier',
        '-title', 'Error',
        '-message', message,
    ])


@contextmanager
def notification_on_error():
    try:
        yield
    except Exception as ex:
        msg = '%s: %s\n' % (type(ex).__name__, ex)
        notify(msg)
        log(msg)
        exit(1)


def get_path_and_line(path, text_after):
    path = re.sub('\.pyc$', '.py', path)
    match = (
        # python stack trace, e.g.
        # File "/path/to/somefile.py", line 336, in some_function
        re.match(r'[^"]*", line (\d+).*', text_after) or
        # ipdb stack trace
        # > /path/to/somefile.py(336)some_function()
        # Fails for
        # /home/dan/nfs-share/website/counsyl/product/data_entry/tests/__init__.py(1005)assertKey()
        re.match(r'[^(]*\((\d+)\).*', text_after) or
        # counsyl/product/api/utils/fake.py:18:1:
        re.match(r'[^:]*:(\d+):\d+:[^:]*', text_after)
    )
    if not match:
        line = 1
        log('%s (no line number)' % path)
        log(path)
        log(text_after)
    else:
        (line,) = match.groups()
        line = int(line)
        log('%s:%d' % (path, line))

    return path, line


def main():
    with notification_on_error():
        path, line = get_path_and_line(*sys.argv[1:])

    with notification_on_error():
        Editor().edit_file(path, line)
