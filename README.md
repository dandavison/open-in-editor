`iterm2-dwim` is a click handler for iTerm2:
you command-click on a file name in the iTerm2 terminal window, and it opens the file in your editor.
If there was a line number, your editor goes to that line.
So, compiler output, tracebacks, etc.

Currently, the only implemented editor backend is Emacs.


### Installation

1. Clone this repo and run `python setup.py develop`.

1. Run `brew install terminal-notifier` and check it's working with `terminal-notifier -message hello`.

1. Make sure that you are starting the emacs server in your emacs config file:
    ```elisp
    (require 'server)
    (unless (server-running-p) (server-start))
    ```

1. Find the absolute path to the `iterm2-dwim` executable, by running the command `which iterm2-dwim`. For example, on my system, this is `/usr/local/bin/iterm2-dwim`.

1. Open iTerm2 settings, find the "Advanced" tab for your iTerm2 profile, and in the "Semantic History" section, choose "Run command" and enter `/absolute/path/to/iterm2-dwim \1 \4`.

Your iTerm2 settings should look something like this:


<img width=600px src="https://user-images.githubusercontent.com/52205/29363274-9e49ba80-828f-11e7-8c80-8790c53ed031.png" alt="image" />


### Debugging

This is under development and you will encounter problems initially.
Probably, you'll command click on something and nothing will happen.

It writes a log. Run `tail -f /tmp/iterm2-dwim.log` in a different terminal window.


| Problem                                                              | Fix                                                                                              |
|----------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| `Command '['which', 'emacsclient']' returned non-zero exit status 1` | Edit `editors/emacs.py` so that it hard codes the absolute path to `emacsclient` on your system. |



### TODO

Currently it only recognizes clicks on absolute file paths starting with a `/`.
It should be possible to make it handle many more types of strings, e.g. relative paths, and random stuff like this that git produces:

```
diff --git a/iterm2_dwim/editors/emacs.py b/iterm2_dwim/editors/emacs.py
```

I think this will involve using iTerm2's [Smart Selection](https://www.iterm2.com/documentation-smart-selection.html) feature, in addition to / instead of Semantic History.
One question there is how to make it convenient to configure the mapping of regexes to actions (where the action is "call `iterm2-dwim` with the relevant context parameters").
The answer may be to use iTerm2's [Dynamic Profiles](https://www.iterm2.com/documentation-dynamic-profiles.html) feature.
