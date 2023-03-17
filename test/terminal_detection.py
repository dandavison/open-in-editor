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

open_in_editor = import_from_file('open-in-editor', 'open-in-editor')
term = open_in_editor.BaseTerminal

def test_terminal_detection():
  test_paths = {
  '/Apps/Wezterm -    In.app/wezterm cli spawn   -- '	:'wezterm',
  '/Apps/Wezterm -    In.app/wezterm cli spawn   -- '	:'wezterm',
  '/usr/local/bin/wezterm  '                         	:'wezterm',
  '/usr/local/bin/wezterm'                           	:'wezterm',
  '/usr/local/bin/wezterm cli spawn -- '             	:'wezterm',
  }
  for path_,bin_ in test_paths.items():
    assert term.infer_terminal_from_path(path_).executable_name == bin_
