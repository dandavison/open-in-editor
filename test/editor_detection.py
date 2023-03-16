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
be = open_in_editor.BaseEditor

def test_editor_detection():
  test_paths = {
  '/Applications/Visual Studio Code - Insiders.app/Contents/Resources/app/bin/code'	:'code',
  '/App/Vis Stu Code -   In.app/app  /bin/code   -g'                               	:'code',
  R'C:\Program Files\Visual Studio Code - Insiders/app/bin/code  - u'              	:'code',
  '/opt/local/bin/hx'                                                              	:'hx',
  'subl   -w'                                                                      	:'subl',
  '/usr/bin/vim   -u'                                                              	:'vim',
  '    vim      -a -b -c'                                                          	:'vim',
  }
  for path_,bin_ in test_paths.items():
    assert be.infer_editor_from_path(path_).executable_name == bin_
