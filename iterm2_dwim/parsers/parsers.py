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
    >>> relative_path('a/b/c.py', 'xxx')
    (CWD + '/a/b/c.py', 1)
    """
    return _parse_relative_path(path_text), 1


def python_stack_trace(path_text, extra_text):
    """
    python stack trace, e.g.
    File "/a/b/c.py", line 2, in some_function

    >>> python_stack_trace('/a/b/c.py', '", line 2, in some_function')
    ('/a/b/c.py', 2)
    """
    regex = r'[^"]*", line (\d+).*'
    line = _parse_line_number(regex, extra_text)
    return path_text, line


def ipdb_stack_trace(path_text, extra_text):
    """
    ipdb stack trace
    > /a/b/c.py(336)some_function()

    >>> ipdb_stack_trace('/a/b/c.py', '(336)some_function()')
    ('/a/b/c.py', 336)
    """
    regex = r'[^(]*\((\d+)\).*'
    line = _parse_line_number(regex, extra_text)
    return path_text, line


def line_and_column(path_text, extra_text):
    """
    counsyl/product/api/utils/fake.py:18:1:

    >>> line_and_column('a/b/c.py', ':18:1:')
    (CWD + '/a/b/c.py', 18)
    """.format(cwd=CWD)

    regex = r':(\d+):\d+.*'
    line = _parse_line_number(regex, extra_text)
    return _parse_relative_path(path_text), line


def git_diff_path(path_text, extra_text):
    """
    `git diff` output contains paths prefixed with a/ and b/:

    diff --git a/a/b/c.py b/a/b/c.py

    >>> git_diff_path('a/a/b/c.py', 'xxx')
    (CWD + '/a/b/c.py', 1)
    >>> git_diff_path('b/a/b/c.py', 'xxx')
    (CWD + '/a/b/c.py', 1)
    """.format(cwd=CWD)

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
