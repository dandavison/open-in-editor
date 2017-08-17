import datetime


LOGFILE = '/tmp/iterm2-dwim.log'


def log(line):
    time = datetime.datetime.now().isoformat(' ').split('.')[0]
    with open(LOGFILE, 'a') as fp:
        fp.write('%s %s\n' % (time, line.encode('utf-8')))
        fp.flush()
