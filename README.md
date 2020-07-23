Open a local file from a URL at a line number in an editor/IDE.

The idea is that you would register this application as a handler for certain URLs in your system.

The URL must be structured like a [file URL](https://en.wikipedia.org/wiki/File_URI_scheme), but it may optionally have a `:<line>:<column>` suffix. If the line is present, the editor will open the file at that line. (Column is ignored currently.)

The URL scheme (protocol) is ignored. For example, you could use standard `file://` URLs, or you could use a custom URL scheme that only exists in your system. In either case, you must register `open-in-editor` (or the provided MacOS application) with your OS as the handler for that URL scheme.

## Examples

```bash
# Using the standard "file://" scheme
open-in-editor 'file:///a/b/myfile.txt'
open-in-editor 'file:///a/b/myfile.txt:7'
open-in-editor 'file:///a/b/myfile.txt:7:77'
open-in-editor 'file://localhost/a/b/myfile.txt:7:77'

# Example of a custom URL scheme:
open-in-editor 'file-line-column:///a/b/myfile.txt'
open-in-editor 'file-line-column:///a/b/myfile.txt:7:77'
```


## Installation

Download the `open_in_editor.py` file from this repo.

Edit `open_in_editor.py` to provide the command to communicate with your editor/IDE (see comments in that file).

Finally, you need to register `open-in-editor.py` with your OS to act as the handler for the URL schemes you are going to use:

### MacOS

1. Use [platypus](https://github.com/sveinbjornt/Platypus) (`brew cask install platypus`) to create a MacOS application wrapping the `open-in-editor` executable. For "Script type" enter the absolute path to the python executable in the `./virtualenv/bin/` directory, and for "Script path" enter the absolute path to the `open-in-editor` executable in the `./virtualenv/bin/` directory.
  <table><tr><td><img width=600px src="https://user-images.githubusercontent.com/52205/88239098-665cda80-cc51-11ea-8f80-ca330a369310.png" alt="image" /></td></tr></table>

2. Use [duti](https://github.com/moretension/duti) (`brew install duti`) to register the MacOS application as the handler for the URL schemes you want it to handle. For example, to make `open-in-editor` handle URLs of the form `file-line-column:///a/b/myfile.txt:7:77`, you would do:

```bash
duti -s <APPLICATION-IDENTIFIER> file-line-column
```

where `<APPLICATION-IDENTIFIER>` is whatever you entered in the "Identifier" field in Platypus.

### Linux
TODO

### Windows
TODO
