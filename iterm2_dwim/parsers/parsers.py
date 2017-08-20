import os
import re

from iterm2_dwim.logger import log


# For relative paths to be handled, add something like the following to shell
# prompt function to inform iterm2-dwim of the current directory:
# echo $PWD > /tmp/cwd
CWD_FILE = '/tmp/cwd'
try:
    with open(CWD_FILE) as fp:
        CWD = fp.read().strip()
except IOError:
    CWD = None


class ParseError(Exception):
    pass


def relative_path(path_text, extra_text):
    """
    Relative path followed by directory.

    This would be via a SmartSelection path regex.
    """
    return _parse_relative_path(path_text), 1


def python_stack_trace(path_text, extra_text):
    # python stack trace, e.g.
    # File "/path/to/somefile.py", line 336, in some_function
    regex = r'[^"]*", line (\d+).*'
    line = _parse_line_number(regex, extra_text)
    return path_text, line


def ipdb_stack_trace(path_text, extra_text):
    # ipdb stack trace
    # > /path/to/somefile.py(336)some_function()
    # Fails for
    # /home/dan/nfs-share/website/counsyl/product/data_entry/tests/__init__.py(1005)assertKey()
    regex = r'[^(]*\((\d+)\).*'
    line = _parse_line_number(regex, extra_text)
    return path_text, line


def line_and_column(path_text, extra_text):
    # counsyl/product/api/utils/fake.py:18:1:
    regex = r':(\d+):\d+.*'
    line = _parse_line_number(regex, extra_text)
    return _parse_relative_path(path_text), line


def git_diff_path(path_text, extra_text):
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


def _parse_relative_path(path_text):
    if not CWD:
        raise ParseError(
            'Got path: %s\n'
            'Interpreting as relative path, but current working '
            'directory unknown.'
        )
    if path_text.startswith('/'):
        raise ParseError

    return os.path.join(CWD, path_text)


PARSERS = [
    python_stack_trace,
    ipdb_stack_trace,
    line_and_column,
    git_diff_path,
    relative_path,
]
