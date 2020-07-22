Open a local file from a URL at a line number in an editor/IDE.

The idea is that you would register this application as a handler for certain URLs in your system.

The URL must be structured like a [file URL](https://en.wikipedia.org/wiki/File_URI_scheme), but it may optionally have a `:<line>:<column>` suffix. If the line is present, the editor will open the file at that line. (Column is ignored currently.)

The URL scheme (protocol) is ignored. For example, you could use standard `file://` URLs, or you could use a custom URL scheme that only exists in your system. In either case, you must register `open-in-editor` (or the provided MacOS application) with your OS as the handler for that URL scheme.

### Examples

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


### Installation

```
git clone git@github.com:dandavison/open-in-editor.git
cd open-in-editor
python3 -m venv virtualenv
./virtualenv/bin/pip install -e .
```

### MacOS

For MacOS, an application bundle `OpenInEditor.app` is provided. This "application bundle" is a normal directory. Inside that directory, you must edit the first line of the file `OpenInEditor.app/Contents/Resources/script` so that it contains the absolute path to the `open-in-editor` executable in the virtualenv.

To register the MacOS application (`org.dandavison.OpenInEditor`) as the handler for a custom URL scheme, you could use [duti](https://github.com/moretension/duti) (`brew install duti`). For example, to make `open-in-editor` handle URLs of the form `file-line-column:///a/b/myfile.txt:7:77`, you would do:

```bash
duti -s org.dandavison.OpenInEditor file-line-column
```
