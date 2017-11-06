#!/usr/bin/env python
# coding: utf_8

import json, requests
import time, sys
import subprocess
import argparse
from pympler import muppy, summary

class main():
    """Requirements: pip install requests.
    You should unsure that mesos-dns is installed on host, where script will be executed. 
    Or you should have a possibility to resolve {leader.mesos}. 
    Check will be executed every 10 seconds.
    Run: 'python3 app.py -h' for help.
    """

    def __init__(self):

        # Set variables:
        self.mesos_master = "leader.mesos"
        self.check_timeout = "60"
        self.get_url = None
        self.json_object = None
        self.framework_dict = {}
        self.framework_inactive_list = []

        # Set Unbuffered stdout
        sys.stdout = Unbuffered(sys.stdout)
        # Parse CLI args
        self.createParser()
        # Initializing
        self.Controller()

    def GetUrl(self):
        try:
            self.get_url = requests.get("http://{}:5050/master/frameworks".format(self.mesos_master))
        except Exception as e:
            print('Could not get url: {}. ERROR: {}'.format(self.mesos_master, e))
            time.sleep(60)
            self.GetUrl()

    def CreateJson(self):
        try:
            self.json_object = json.loads(self.get_url.text)
        except Exception as e:
            print('Could not serialize to json format. ERROR: {}'.format(e))

    def CreateFrameworkDict(self):
        for framework in self.json_object['frameworks']:
            self.framework_dict[framework['id']] = {framework['name']: framework['active']}
            if not framework['active']:
                self.framework_inactive_list.append(framework['id'])

    def RemoveMesosFramework(self):
        for framework in self.framework_inactive_list:
            print("Framework_id: {} will be shutdown".format(framework))

            first = ["echo", "frameworkId={}".format(framework)]
            second = ["curl", "-d@-", "-X", "POST", "http://{}:5050/master/teardown".format(self.mesos_master)]
            p1 = subprocess.Popen(first, stdout=subprocess.PIPE)
            p2 = subprocess.Popen(second, stdin=p1.stdout, stdout=subprocess.PIPE)

    def createParser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-m', '--mesos_host', default='leader.mesos', help='Specify mesos master host')
        parser.add_argument('-t', '--timeout', default='60', help='Set check timeout')
        self.check_timeout = parser.parse_args().timeout
        self.mesos_master = parser.parse_args().mesos_host

    def Controller(self):
        while True:
            self.GetUrl()
            self.CreateJson()
            self.CreateFrameworkDict()
            if self.framework_inactive_list:
                self.RemoveMesosFramework()
                del self.framework_inactive_list[:]
#                self.memory_check()
            else:
                print("Keep watching. No frameworks in inactive state")
#                self.memory_check()
            time.sleep(int("{}".format(self.check_timeout)))

    def memory_check(self):
        '''This func adds ability to measure memory consumption by all objects'''
        all_objects = muppy.get_objects()
        sum = summary.summarize(all_objects)
        summary.print_(sum)


class Unbuffered(object):
    """This Class give a possibility not to buffer stdout.
    It helps execute print statement immediately.
    """

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


if __name__ == "__main__":
    run = main()


