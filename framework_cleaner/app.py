import json, requests
import time
import subprocess

class main():

    """You should unsure that mesos-dns is installed on host, where script will be executed. 
    Or you should have a possibility to resolve {leader.mesos}. 
    Check will be executed every 10 seconds.
    """

    def __init__(self):

        # Set variables:
        self.mesos_url = "m1-qa1.dev.whirl.sg:5050"
        self.get_url = None
        self.json_object = None
        self.framework_dict = {}
        self.framework_inactive_list = []

        # Initializing
        self.Controller()

    def GetUrl(self):
        try:
            self.get_url = requests.get("http://{}/master/frameworks".format(self.mesos_url))
        except Exception as e:
            print('Could not get url: {}. ERROR: {}'.format(self.mesos_url, e))

    def CreateJson(self):
        try:
            self.json_object = json.loads(self.get_url.text)
        except Exception as e:
            print('Could not serialize to json format. ERROR: {}'.format(e))

    def CreateFrameworkDict(self):
        for framework in self.json_object['frameworks']:
            self.framework_dict[framework['id']] = {framework['name']:framework['active']}
            if not framework['active']:
                self.framework_inactive_list.append(framework['id'])

    def RemoveMesosFramework(self):
        for framework in self.framework_inactive_list:
            print("Framework_id: {} will be removed".format(framework))

            first = ["echo", "frameworkId={}".format(framework)]
            second = ["curl", "-d@-", "-X", "POST", "http://{}/master/teardown".format(self.mesos_url)]
            p1 = subprocess.Popen(first, stdout=subprocess.PIPE)
            p2 = subprocess.Popen(second, stdin=p1.stdout, stdout=subprocess.PIPE)
            print(p2.stdout.read())

    def Controller(self):
        while True:
            self.GetUrl()
            self.CreateJson()
            self.CreateFrameworkDict()
            time.sleep(10)
            if self.framework_inactive_list:
                self.RemoveMesosFramework()


if __name__ == "__main__":
        run = main()


