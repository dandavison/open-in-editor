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


class Rule(object):
    """
    Subclasses must implement self._parse(path_text, extra_text).
    self._parse must set self.path and may set self.line.
    """

    def __init__(self):
        self.path = None
        self.line = None

    def parse(self, path_text, extra_text):

        self._parse(path_text, extra_text)

        if not self.path:
            raise ParseError()

        if not self.path.startswith('/'):
            if not CWD:
                raise ParseError(
                    'Got path: %s\n'
                    'Interpreting as relative path, but current working '
                    'directory unknown.'
                )
            self.path = os.path.join(CWD, self.path)

        if not os.path.exists(self.path):
            raise ParseError()

        if not self.line:
            self.line = 1

        return self.path, self.line


class Path(Rule):
    """
    The simplest rule: accept the path_text without change and don't look for a
    line number.

    >>> Path().parse('a/b/c.py', 'xxx')
    ('a/b/c.py', 1)
    """
    def _parse(self, path_text, extra_text):
        self.path = path_text


class ExtraTextLineRegexRule(Rule):
    """
    Base class for rules employing a regex to extract the line number from the
    `extra_text`.
    """
    regex = None

    def _parse(self, path_text, extra_text):
        self.path = path_text
        self.line = self._parse_line_number(extra_text)

    def _parse_line_number(self, text):
        match = re.match(self.regex, text)
        if not match:
            raise ParseError()
        (line,) = match.groups()
        return int(line)


class PythonStackTrace(ExtraTextLineRegexRule):
    """
    python stack trace, e.g.
    File "/a/b/c.py", line 2, in some_function

    >>> PythonStackTrace().parse('/a/b/c.py', '", line 2, in some_function')
    ('/a/b/c.py', 2)
    """
    regex = r'[^"]*", line (\d+).*'


class IpdbStackTrace(ExtraTextLineRegexRule):
    """
    ipdb stack trace
    > /a/b/c.py(336)some_function()

    >>> IpdbStackTrace().parse('/a/b/c.py', '(336)some_function()')
    ('/a/b/c.py', 336)
    """
    regex = r'[^(]*\((\d+)\).*'


class CompilerOutput(ExtraTextLineRegexRule):
    """
    counsyl/product/api/utils/fake.py:18:1:

    >>> CompilerOutput().parse('a/b/c.py', ':18:1:')
    ('a/b/c.py', 18)
    """
    regex = r':(\d+):\d+.*'


class GitDiffOutput(Rule):
    """
    `git diff` output contains paths prefixed with a/ and b/:

    diff --git a/a/b/c.py b/a/b/c.py

    >>> GitDiffOutput().parse('a/a/b/c.py', 'xxx')
    ('a/b/c.py', 1)
    >>> GitDiffOutput().parse('b/a/b/c.py', 'xxx')
    ('a/b/c.py', 1)
    """
    def _parse(self, path_text, extra_text):
        if (path_text.startswith('a/') or path_text.startswith('b/')):
            self.path = path_text[2:]
        else:
            raise ParseError


RULES = [
    PythonStackTrace(),
    IpdbStackTrace(),
    CompilerOutput(),
    GitDiffOutput(),
    Path(),
]
