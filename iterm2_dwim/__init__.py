#!/usr/bin/env python
from datetime import datetime
from contextlib import contextmanager
import os
import re
import subprocess
import sys


LOG = '/tmp/iterm2-dwim.log'
EMACSCLIENT = '/usr/local/bin/emacsclient'


def notify(message):
    subprocess.check_call([
        '/usr/local/bin/terminal-notifier',
        '-title', 'Error',
        '-message', message,
    ])


def log(line):
    time = datetime.now().isoformat(' ').split('.')[0]
    with open(LOG, 'a') as fp:
        fp.write('%s %s\n' % (time, line))
        fp.flush()


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


def edit_file(path, line):
    cmd = [
        EMACSCLIENT,
        '--no-wait',
        '--eval', '(find-file "%s")' % path,
        '--eval', '(select-frame-set-input-focus (selected-frame))',
        '--eval', '(goto-line %d)' % line,
    ]
    log(cmd)
    subprocess.check_call(cmd)


def main():
    with notification_on_error():
        path, line = get_path_and_line(*sys.argv[1:])

    with notification_on_error():
        edit_file(path, line)
