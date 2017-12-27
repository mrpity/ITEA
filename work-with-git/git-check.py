#!/usr/bin/env python
#coding: utf_8

import requests
from requests.auth import HTTPBasicAuth
import subprocess
import re

class main():
    """
    Behaviour:
    - Check git changes
    - Run jenkins job

    This class covers 3 git endpoints to check for changes (folders in root dir of repository):
    1) 'be'
    2) 'edr'
    3) 'common'

    Specific 'jenkins job' and 'jenkins job token', 'jenkins user' and 'auth token', 'build  parameters' are set in __init__ func.
    """

    def __init__(self):

        self.BE_ENDPOINT = 'be'
        self.EDR_ENDPOINT = 'edr'
        self.COMMON_ENDPOINT = 'common'

        self.JENKINS_ENDPOINT_JOB = 'http://jenkins.wmed.whirl.sg/view/PULLREQUESTCI-WMED/job/pull-request-ci'
        self.JENKINS_ENDPOINT_JOB_TOKEN = 'pull-request-check'
        self.JENKINS_ENDPOINT_TEMP = '{}/buildWithParameters?token={}&' +\
                                                               'COMMIT={}&' +\
                                                               'COMPONENT_WMED_EDR={}&' +\
                                                               'COMPONENT_WMED_BE={}&' +\
                                                               'COMPONENT_WMED_COMMON={}'
        self.JENKINS_USER = 'jenkinsci'
        self.JENKINS_TOKEN = '6a70033c98183a92f226e4c982120f85'

        self.FILE_NAME = 'envs.properties'
        self.ENDPOINT_DICT = { self.BE_ENDPOINT:False, self.EDR_ENDPOINT:False, self.COMMON_ENDPOINT: False } # Dict of endpoints where changes happened. Default: False

        ''' Execution '''
        self.git_files = self.get_git_data()
        self.changed_files = self.form_list_of_files()
        self.git_commit = self.get_git_commit_rev()
        self.check_git_changes()

    # Get all changed files from git under current git revision
    def get_git_data(self):
        git_data = ["git", "show", "--pretty=", "--name-only"]
        p = subprocess.Popen(git_data, stdout=subprocess.PIPE)
        return p.stdout.read().decode("utf-8")

    # Retrive the hash for current commit
    def get_git_commit_rev(self):
        git_hash = ["git", "rev-parse", "HEAD"]
        p = subprocess.Popen(git_hash, stdout=subprocess.PIPE)
        return p.stdout.read().decode("utf-8").strip()

    # Formed list of changed git files. Delimeter: \n
    def form_list_of_files(self):
        changed_files = self.git_files.split("\n")
        print("ALL CHANGED FILES: {}".format(changed_files))
        return changed_files

    # Function will check if something is changed in BE_ENDPOINT, EDR_ENDPOINT, COMMON_ENDPOINT folders
    def check_git_changes(self):
        for item in self.changed_files:
            if item.startswith('{}'.format(self.BE_ENDPOINT)):
                self.ENDPOINT_DICT[self.BE_ENDPOINT] = True
                self.write_to_groovy_file(self.BE_ENDPOINT, self.ENDPOINT_DICT[self.BE_ENDPOINT])
            else:
                self.ENDPOINT_DICT[self.BE_ENDPOINT] = False
                self.write_to_groovy_file(self.BE_ENDPOINT, self.ENDPOINT_DICT[self.BE_ENDPOINT])
            if item.startswith('{}'.format(self.EDR_ENDPOINT)):
                self.ENDPOINT_DICT[self.EDR_ENDPOINT] = True
                self.write_to_groovy_file(self.EDR_ENDPOINT, self.ENDPOINT_DICT[self.EDR_ENDPOINT])
            else:
                self.ENDPOINT_DICT[self.EDR_ENDPOINT] = False
                self.write_to_groovy_file(self.EDR_ENDPOINT, self.ENDPOINT_DICT[self.EDR_ENDPOINT])
            if item.startswith('{}'.format(self.COMMON_ENDPOINT)):
                self.ENDPOINT_DICT[self.COMMON_ENDPOINT] = True
                self.write_to_groovy_file(self.COMMON_ENDPOINT, self.ENDPOINT_DICT[self.COMMON_ENDPOINT])
            else:
                self.ENDPOINT_DICT[self.COMMON_ENDPOINT] = False
                self.write_to_groovy_file(self.COMMON_ENDPOINT, self.ENDPOINT_DICT[self.COMMON_ENDPOINT])

    # Create Jenkins JOB URL with parameters
    def create_jenkins_url(self):
        return self.JENKINS_ENDPOINT_TEMP.format(self.JENKINS_ENDPOINT_JOB, self.JENKINS_ENDPOINT_JOB_TOKEN, self.git_commit, self.ENDPOINT_DICT['be'], self.ENDPOINT_DICT['edr'], self.ENDPOINT_DICT['common'])

    # RUN JENKINS JOB
    def run_jenkins_job(self):
        JENKINS_ENDPOINT = self.create_jenkins_url()
        print(JENKINS_ENDPOINT)
        print(requests.get('{}'.format(JENKINS_ENDPOINT), auth=HTTPBasicAuth('{}'.format(self.JENKINS_USER), '{}'.format(self.JENKINS_TOKEN))))

    # Create file with envs
    def write_to_groovy_file(self, COMPONENT, STATUS):

        # Repalce old values in file self.F_NAME
        sourceText= "env.{}.*[\n]?".format(COMPONENT)     # [\n]? -- 0 or 1 time; .* -- any symbol 0 or more times.
        self.ReplaceLineInFile(sourceText,'')

        file_name = "{}".format(self.FILE_NAME)
        with open('{}'.format(file_name), 'a') as f:
            f.write("env.{}='{}'\n".format(COMPONENT, STATUS))

    # Func for replacing old values
    def ReplaceLineInFile(self, sourceText, replaceText):
        try:
            file = open(self.FILE_NAME, 'r')
            text = file.read()
            file.close()
        except IOError:
            print ("File: {} is not found. Creating it...".format(self.FILE_NAME))
            f = open(self.FILE_NAME, 'w')
            f.close()
            file = open(self.FILE_NAME, 'r')
            text = file.read()
            file.close()
            pass
        file = open(self.FILE_NAME, 'w')
        file.write(re.sub(sourceText, replaceText.strip(), text))
        file.close()


    def controller(self):
        pass

if __name__ == '__main__':
    run = main()
    run.write_to_groovy_file("COMMIT", run.git_commit)
    #run.run_jenkins_job() # Trigger job by token
    print(run.ENDPOINT_DICT)
    print(run.git_commit)


