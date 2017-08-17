`iterm2-dwim` is a click handler for iTerm2:
you command-click on a file name in the iTerm2 terminal window, and it opens the file in your editor.
If there was a line number, your editor goes to that line.
So, compiler output, tracebacks, etc.

Currently, Emacs and Sublime are supported. To select an editor, enter "emacs" or "sublime" as the editor in "settings.py" and enter the path to `emacsclient` or `subl`.

### Installation

1. Run `brew install terminal-notifier` and check it's working with `terminal-notifier -message hello`.

1. (Optional, but relative paths won't be resolved without it): configure your shell prompt so that the current directory is written to a file named `/tmp/cwd` every time the prompt is displayed.
    For example, put this line in your `~/.bashrc`:
    ```sh
    export PROMPT_COMMAND='echo $PWD > /tmp/cwd'
    ```

1. Make sure that you are starting the emacs server in your emacs config file:
    ```elisp
    (require 'server)
    (unless (server-running-p) (server-start))
    ```

1. Clone this repo and run `python setup.py develop`.

1. Find the absolute path to the `iterm2-dwim` executable, by running the command `which iterm2-dwim`. For example, on my system, this is `/usr/local/bin/iterm2-dwim`.

1. Open iTerm2 settings, find the "Advanced" tab for your iTerm2 profile, and do two things:
   1. In the "Smart Selection" section, click "Edit", select the "Paths" rule, click "Edit Actions", choose "Run Command" and enter `/usr/local/bin/iterm2-dwim \0 \d`.
   1. In the "Semantic History" section, choose "Run command" and enter `/absolute/path/to/iterm2-dwim \1 \4`.

Your iTerm2 settings should look something like this:


<img width=600px src="https://user-images.githubusercontent.com/52205/29363274-9e49ba80-828f-11e7-8c80-8790c53ed031.png" alt="image" />

<img width=600px src="https://user-images.githubusercontent.com/52205/29406054-2df3f8b6-8340-11e7-9996-64a0f873da5c.png" alt="image" />


### Debugging

This is under development and you will encounter problems initially.
Probably, you'll command click on something and nothing will happen.

It writes a log. Run `tail -f /tmp/iterm2-dwim.log` in a different terminal window.


| Problem                                                              | Fix                                                                                              |
|----------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| `Command '['which', 'emacsclient']' returned non-zero exit status 1` | Edit `editors/emacs.py` so that it hard codes the absolute path to `emacsclient` on your system. |
