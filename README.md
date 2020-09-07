Open a local file from a URL at a line number in an editor/IDE.

The idea is that you would register this application as a handler for certain URLs in your system.

The URL must be structured like a [file URL](https://en.wikipedia.org/wiki/File_URI_scheme), but it may optionally have a `:<line>:<column>` suffix. If the line is present, the editor will open the file at that line. (Column is currently only implemented for vim.)

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

Download the `open-in-editor` file from this repo and make it executable.

Ensure that one of the environment variables `OPEN_IN_EDITOR` or `EDITOR` contains a path to an executable that `open-in-editor` is going to recognize. This environment variable must be set system-wide, not just in your shell process. For example, in MacOS, one does this with `launchctl setenv EDITOR /path/to/my/editor/executable`.

`open-in-editor` looks for any of the following substrings in the path: `emacsclient` (emacs), `subl` (sublime), `charm` (pycharm), `code` (vscode) or `vim` (vim). For example, any of the following values would work:

- `/usr/local/bin/emacsclient`
- `/usr/local/bin/charm`
- `/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl`
- `/usr/local/bin/code`
- `/usr/bin/vim`
- `/usr/local/bin/nvim`

If your editor/IDE isn't supported, then please open an issue. If your editor/IDE is supported, but the above logic needs to be made more sophisticated, then either (a) open an issue, or (b) create a symlink that complies with the above rules.

Next, you need to register `open-in-editor` with your OS to act as the handler for the URL schemes you are going to use:

### MacOS app

For MacOS, an application bundle `OpenInEditor.app` is provided.

Use [duti](https://github.com/moretension/duti) (`brew install duti`) to register the MacOS application (`org.dandavison.OpenInEditor`) as the handler for the URL schemes you want it to handle. For example, to make `open-in-editor` handle URLs of the form `file-line-column:///a/b/myfile.txt:7:77`, you would do:

```bash
duti -s org.dandavison.OpenInEditor file-line-column
```

### Linux

On a system that complies to the [XDG shared MIME-info DB specification](https://specifications.freedesktop.org/shared-mime-info-spec/shared-mime-info-spec-latest.html#idm140625828587776), there are two simple steps to follow. This should apply to the majority of current GNU/Linux installations - if you're unsure check if `type -P xdg-mime` returns a file path.

First, you need to create a `.desktop` file which references `open-in-editor`, and then set that as default for either the `file-line-column://` or the `file://` URL scheme, depending on your choice. For example execute the following commands in a shell :

```sh
$ cat >~/.local/share/applications/augmented-open.desktop <<OVER
[Desktop Entry]
Type=Application
Name=AugmentedOpen
GenericName=Open a file at a certain position
Comment=Opens URLs of the type file-line-column://<path>[:<line>[:<column>]] in the configured editor and positions the cursor
Icon=text-editor
Exec=open-in-editor %U
Categories=Utility;Core;
StartupNotify=false
MimeType=x-scheme-handler/file-line-column
OVER

$ xdg-mime default augmented-open.desktop x-scheme-handler/file-line-column
```

Alternatively, you can register the URL scheme system wide (i.e. for _every_ user); just run those two shell commands as the root user (e.g. prefix them with `sudo`) and replace `~/.local/...` with `/usr/local/...` in the topmost line.

If you'd rather overwrite the default `file://` URL scheme, just replace every instance of `file-line-column` with just `file`.

Remember to define the `EDITOR` (resp. `OPEN_IN_EDITOR`) variable in your environment, if you haven't already done so.

You can now use this type of URLs with `xdg-open file[-line-column]://<path>[:line[:column]]` or - in case you run a desktop environment which supports it - by clicking on such a URL just like you would with a web link.

TODO: automation (makefile/script)

### Windows
TODO
