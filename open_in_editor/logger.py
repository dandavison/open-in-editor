import datetime


LOGFILE = "/tmp/open-in-editor.log"


def log(line):
    time = datetime.datetime.now().isoformat(" ").split(".")[0]
    with open(LOGFILE, "a") as fp:
        print(time, file=fp)
        print(line, file=fp)
        print("\n", file=fp)
        fp.flush()
