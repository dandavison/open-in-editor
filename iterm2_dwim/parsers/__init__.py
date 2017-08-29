import os

from iterm2_dwim.logger import log
from iterm2_dwim.parsers import parsers


def get_path_and_line(path_text, extra_text=''):
    for rule in parsers.RULES:
        log(rule.__class__.__name__)
        try:
            return rule.parse(path_text, extra_text)
        except parsers.ParseError:
            continue

    raise parsers.ParseError('No matching rule')
