import os
import re

from iterm2_dwim.logger import log


# For relative paths to be handled, add something like the following to shell
# prompt function to inform iterm2-dwim of the current directory:
# echo $PWD > /tmp/cwd
CWD_FILE = '/tmp/cwd'


class ParseError(Exception):
    pass


def relative_path(path_text, text_after):
    """
    Relative path followed by directory.

    This would be via a SmartSelection path regex.
    """
    if path_text.startswith('/'):
        raise ParseError

    try:
        with open(CWD_FILE) as fp:
            cwd = fp.read().strip()
    except IOError:
        raise ParseError(
            'Got path: %s\n'
            'Interpreting as relative path, but current working '
            'directory unknown.'
        )
    else:
        return os.path.join(cwd, path_text), 1


def python_stack_trace(path_text, text_after):
    # python stack trace, e.g.
    # File "/path/to/somefile.py", line 336, in some_function
    regex = r'[^"]*", line (\d+).*'
    line = _parse_line_number(regex, text_after)
    return path_text, line


def ipdb_stack_trace(path_text, text_after):
    # ipdb stack trace
    # > /path/to/somefile.py(336)some_function()
    # Fails for
    # /home/dan/nfs-share/website/counsyl/product/data_entry/tests/__init__.py(1005)assertKey()
    regex = r'[^(]*\((\d+)\).*'
    line = _parse_line_number(regex, text_after)
    return path_text, line


def line_and_column(path_text, text_after):
    # counsyl/product/api/utils/fake.py:18:1:
    regex = r'[^:]*:(\d+):\d+:[^:]*'
    line = _parse_line_number(regex, text_after)
    return path_text, line


def git_diff_path(path_text, text_after):
    if not (path_text.startswith('a/') or
            path_text.startswith('b/')):
        raise ParseError
    return relative_path(path_text[2:], None)


def _parse_line_number(regex, text):
    match = re.match(regex, text)
    if not match:
        raise ParseError()
    (line,) = match.groups()
    return int(line)


PARSERS = [
    relative_path,
    python_stack_trace,
    ipdb_stack_trace,
    line_and_column,
    git_diff_path,
]
