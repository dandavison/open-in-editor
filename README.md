`iterm2-dwim` is a click handler for iTerm2: you command-click on a file name in the iTerm2 terminal window, and it opens the file in your editor. If there was a line number, your editor goes to that line. So, compiler output, tracebacks, etc.

Currently, it works with emacs only.


**Installation**

1. Clone this repo and run `python setup.py develop`.

2. Find the absolute path to the `iterm2-dwim` executable, by running the command `which iterm2-dwim`. For example, on my system, this is `/usr/local/bin/iterm2-dwim`.

3. Open iTerm2 settings, find the "Advanced" tab for your iTerm2 profile, and in the "Semantic History" section, choose "Run command" and enter `/absolute/path/to/iterm2-dwim \1 \4`.

Your iTerm2 settings should look something like this:


<img width=600px src="https://user-images.githubusercontent.com/52205/29363274-9e49ba80-828f-11e7-8c80-8790c53ed031.png" alt="image" />
