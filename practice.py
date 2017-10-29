import sys, os
import pprint
from threading import Thread
from queue import Queue
import tailer
import time
from pygtail import Pygtail



if __name__ == '__main__':

    log_file_to_monitor='/tmp/syslog.log'
#    sys.exit(14)

    def tail(f):
        f.seek(0, 2)

        while True:
            line = f.readline()

            if not line:
                time.sleep(0.1)
                continue

            yield line


    def process_matches(matchtext):
        while True:
            line = yield
            print(line)
            print(type(line))
            if matchtext in line:
                do_something_useful()  # email alert, etc.

    def do_something_useful():
        print('HO-HO-HO')

    list_of_matches = ['ERROR', 'CRITICAL']
    matches = [process_matches(string_match) for string_match in list_of_matches]
    print(matches)

    for m in matches:  # prime matches
        m.__next__()

    while True:
        auditlog = tail(open(log_file_to_monitor))
        for line in auditlog:
            for m in matches:
                m.send(line)