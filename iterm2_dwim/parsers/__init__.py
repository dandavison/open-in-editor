import re

from iterm2_dwim.logger import log
from iterm2_dwim.parsers.parsers import PARSERS
from iterm2_dwim.parsers.parsers import ParseError


def get_path_and_line(path, text_after):
    path = re.sub('\.pyc$', '.py', path)

    for parse_fn in PARSERS:
        log(parse_fn.__name__)
        try:
            return parse_fn(path, text_after)
        except ParseError as ex:
            log(ex)
            continue

    return path, 1
