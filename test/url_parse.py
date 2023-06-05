import os
import sys
import inspect
import importlib.util
from importlib.machinery import SourceFileLoader

curdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
pardir = os.path.dirname(curdir)
sys.path.insert(0, pardir)


def import_from_file(module_name, file_path):
  loader = SourceFileLoader(module_name, file_path)
  spec   = importlib.util.spec_from_file_location(module_name, loader=loader)
  module = importlib.util.module_from_spec(spec)
  sys.modules[module_name] = module
  spec.loader.exec_module(module)

  return module

open_in_editor = import_from_file('open-in-editor', 'OpenInEditor.app/Contents/Resources/script')
parse_url = open_in_editor.parse_url

def test_editor_detection():
  test_urls = {
  'a%20b.txt'	:'a b.txt',
  }
  for url_escaped,url_raw in test_urls.items():
    assert parse_url(url_escaped)[0] == url_raw
