import json, requests
import time, datetime

class main():

    def __init__(self):

        # Set variables:
        self.mesos_url = "http://m1-qa1.dev.whirl.sg:5050/master/frameworks"
        self.get_url = None
        self.json_object = None
        self.framework_dict = {}
        self.framework_inactive_list = []

        # Initializing
        self.Controller()

    def GetUrl(self):
        try:
            self.get_url = requests.get(self.mesos_url)
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
            # link_to_remove = 'echo "frameworkId={}" | curl -d@- -X POST http://leader.mesos:5050/master/teardown'.format(framework)
            print("Framework_id: {} will be removed".format(framework))

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


