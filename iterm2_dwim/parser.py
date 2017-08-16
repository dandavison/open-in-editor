import os
import re

from iterm2_dwim.logger import log


def get_path_and_line(path, text_after):
    if not path.startswith('/') and text_after.startswith('/'):
        # Hack: relative path followed by directory
        # SmartSelection path regex passing \0 \d
        return os.path.join(text_after, path), 1

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
