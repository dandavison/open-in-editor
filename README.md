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
To support terminal editors like `vim` ensure that environment variables `TERMINAL` is set to the path of the terminal executable that will open the editor.

`open-in-editor` looks for any of the following substrings in the editor path: `emacsclient` (emacs), `subl` (sublime), `charm` (pycharm), `code` (vscode), `vim` (vim) or `o` (o). For example, any of the following values would work:

- `/usr/local/bin/emacsclient`
- `/usr/local/bin/charm`
- `/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl`
- `/Applications/Visual Studio Code - Insiders.app/Contents/Resources/app/bin/code`
- `/usr/local/bin/code`
- `/usr/bin/vim`
- `/usr/local/bin/nvim`
- `/usr/bin/o`

...and for any of the following substrings in the terminal path: `wezterm` (WezTerm)

If your editor/IDE/terminal isn't supported, then please open an issue or file a PR. If your editor/IDE is supported, but the above logic needs to be made more sophisticated, then either (a) open an issue, or (b) create a symlink that complies with the above rules.

Next, you need to register `open-in-editor` with your OS to act as the handler for the URL schemes you are going to use:

### MacOS

For MacOS, an application bundle `OpenInEditor.app` is provided.

Use [duti](https://github.com/moretension/duti) (`brew install duti`) to register the MacOS application (`org.dandavison.OpenInEditor`) as the handler for the URL schemes you want it to handle. For example, to make `open-in-editor` handle URLs of the form `file-line-column:///a/b/myfile.txt:7:77`, you would do:

```bash
duti -s org.dandavison.OpenInEditor file-line-column
```

Alternatively, you can easily install `open-in-editor` with _[Homebrew](https://brew.sh) ([Cask](https://docs.brew.sh/Cask-Cookbook)), which already includes the above steps:_
```rb
brew tap dandavison/open-in-editor https://github.com/dandavison/open-in-editor.git
brew install --cask open-in-editor
```

Also, if you keep a [_Brewfile_](https://github.com/Homebrew/homebrew-bundle#usage), you can add something like this:
```rb
repo = "dandavison/open-in-editor"
tap repo, "https://github.com/#{repo}.git"
cask "open-in-editor"
```

### Arch Linux

The Repository contains a pacman ``PKGBUILD`` file. To install it run from the root of the directory, or any directory that contains the ``PKGBUILD`` file.

```sh
makepkg --install
```

Then just register it with:

```sh
xdg-mime default open-in-editor.desktop x-scheme-handler/file-line-column
```

### Linux

On a system that complies with the [XDG shared MIME-info DB specification](https://specifications.freedesktop.org/shared-mime-info-spec/shared-mime-info-spec-latest.html#idm140625828587776), you can follow the steps below. This should apply to the majority of current GNU/Linux installations - if you're unsure, run `type -P xdg-mime` and check that it returns a file path.

1. Create the directory `~/.local/share/applications/`, if it doesn't exist already.

2. Create the file `~/.local/share/applications/augmented-open.desktop` and add the following contents to it:
   ```
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
   ```

3. Run the command
   ```
   xdg-mime default augmented-open.desktop x-scheme-handler/file-line-column
   ```
   This registers the `augmented-open.desktop` handler as the default handler for URLs using the `file-line-column://` protocol.

The string used for the URL protocol is up to you: if you want to use `open-in-editor` to handle `file://` URLs, then replace `file-line-column` with `file` in the above instructions.

If you want to register the URL handler system-wide (i.e. for _every_ user) then create the file at `/usr/local/...` instead of `~/.local/...`. You will need to use `sudo` to perform the commands since they will need root permissions.

Remember to define the `EDITOR` or `OPEN_IN_EDITOR` environment variable, if you haven't already done so.

You can now use these URLs by clicking on them in applications just like you would with a web link. From the command line, use `xdg-open file[-line-column]://<path>[:line[:column]]`.

### Windows
TODO
