#!/usr/bin/env python
#coding: utf_8

import sys, json, argparse, httplib
import configparser
from xml.dom import minidom
import requests
import re
import operator

class main():

    def __init__(self, ET, CONF_DIR, F_NAME):
        self.ET = ET
        self.CONF_DIR = CONF_DIR
        self.F_NAME = F_NAME

        self.GetCOMMON = self.getCommonFile()                      # Get all COMMON vars from conf file
        self.GetSERVICELIST = self.getServiceList()                # Get list of services for installation
        self.GetServiceVars = None                                 # Get all SERVICE vars from conf file

        self.SERVICE_REPO = None
        self.SERVICE_ARTIFACT_ID = None
        self.SERVICE_GROUP_ID = None

        self.addr = None            # XML instance from getXML func
        self.RE='.*CI([0-9]+).*'    # Regular Expression. grep all versions like 3.9_cds-be_CI195-SNAPSHOT, 3.9_cds-be_CI204-SNAPSHOT
        self.artifact_dict = None
        self.latest_artifact= None

    def getConfig(self):

        ### Include conf file according to TYPE
        config = configparser.ConfigParser()
        conf_dir = '{}/{}.ini'.format(self.CONF_DIR , self.ET)
        config.read(conf_dir)                                       # include conf file in the same dir with main script. Default path: .

        return config

    def getCommonFile(self):

        config = self.getConfig()
        ### Check if conf file exists and options in conf file exist
        try:
            self.GetCOMMON = config['COMMON']
        except Exception:
            print("ERROR. Cann't find config COMMON in file: {}. Maybe this file doesn't exist".format(self.CONF_DIR))
            
        return self.GetCOMMON

    ### Just get list of services
    def getServiceList(self):

        config = self.getConfig()
        ### Check if conf file exists and options in conf file exist
        try:
            GetServiceList = config['COMMON']
        except Exception:
            print("ERROR. Cann't find config COMMON in file: {}. Maybe this file doesn't exist".format(self.CONF_DIR))

        ### Create list from vars that are taken from conf file
        SERVICE_LIST = []
        for item in GetServiceList['SERVICE_LIST'].split(','):
            SERVICE_LIST.append(item.encode('ascii').strip())

        return SERVICE_LIST

    def getServiceVars(self, SERVICE):

        config = self.getConfig()
        ### Check if conf file exists and options in conf file exist
        try:
            self.GetServiceVars = config['{}'.format(SERVICE)]
        except Exception:
            print("ERROR. Cann't find config COMMON in file: {}. Maybe this file doesn't exist".format(self.CONF_DIR))

        ### Set vars according to service type(item): CDS_BE, WAS....
        self._createServiceVars()

        return self.GetServiceVars

    def _createServiceVars(self):

        ### Set vars from conf file
        self.SERVICE_REPO = self.GetServiceVars['SERVICE_REPO']
        self.SERVICE_ARTIFACT_ID = self.GetServiceVars['SERVICE_ARTIFACT_ID']
        self.SERVICE_GROUP_ID = self.GetServiceVars['SERVICE_GROUP_ID']

    def getXML(self):
        ARTIFACTORY = self.GetCOMMON['URL']

        ### From direct link for meven-metadata.xml from artifactory
        artifactory_link = '{}/{}/{}/{}/maven-metadata.xml'.format(ARTIFACTORY,self.SERVICE_REPO,self.SERVICE_GROUP_ID,self.SERVICE_ARTIFACT_ID )
        addr = requests.get(artifactory_link)

        ### Raise exception if there is no access to maven-metadata.xml
        if addr.status_code != 200:
            print("ERROR.Cann't get access to {}, code status: {}".format(artifactory_link,addr.status_code))
            raise SystemExit(1)
        return addr

    ### Create dict from unique artifact list for get the max/latest value from it
    def create_artifact_dict(self):

        self.addr = self.getXML()
        maven_xml = minidom.parseString(self.addr.text)
        versions = maven_xml.getElementsByTagName("version")

        artifact_list = []
        for version in versions:
            artifact_list.append(version.childNodes[0].nodeValue)

        artifact_list = set(artifact_list)   # get only unique values

        artifact_dict = {}
        for item in artifact_list:
            pattern_match = re.match(r'{}'.format(self.RE), item)
            if pattern_match:
                artifact_dict[pattern_match.group(1)] = item

        self.artifact_dict = artifact_dict

        return self.artifact_dict

    ### Get the latest artifact from dict that is mentioned above
    def get_latest_artifact(self):

        latest_version = max(self.artifact_dict.iteritems(), key=operator.itemgetter(1))[0]
        latest_artifact = self.artifact_dict[latest_version]

        ### Check if var:latest_artifact isn't empty
        if not latest_artifact:
            print ("ERROR. latest_artifact var is empty: {}".format(latest_artifact))
            raise SystemExit(1)

        return latest_artifact

    ### Write latest_artifact to file. SERVICE --
    def write_to_file(self, SERVICE):

        # Repalce old values in file self.F_NAME
        sourceText= "{}.*[\n]?".format(SERVICE)     # [\n]? -- 0 or 1 time; .* -- any symbol 0 or more times.
        self.ReplaceLineInFile(sourceText,'')

        self.latest_artifact = self.get_latest_artifact()

        file_name = "{}".format(self.F_NAME)
        f = open('{}'.format(file_name), 'a')
        f.write('{}={}\n'.format(SERVICE, self.latest_artifact))
        f.close()

    def ReplaceLineInFile(self, sourceText, replaceText):
        try:
            file = open(self.F_NAME, 'r')
            text = file.read()
            file.close()
        except IOError:
            print 'File: {} is not found. Creating it'.format(self.F_NAME)
            f = open(self.F_NAME, 'w')
            f.close()
            file = open(self.F_NAME, 'r')
            text = file.read()
            file.close()
            pass
        file = open(self.F_NAME, 'w')
        file.write(re.sub(sourceText, replaceText.strip(), text))
        file.close()

if __name__ == '__main__':

    ### Parse CLI vars
    def createParser():
        parser = argparse.ArgumentParser()
        #    parser.add_argument('-n','--et_name', required=True, help='Set engineering team name: ET2, ET1')
        parser.add_argument('-d', '--directory', default='.', help='Path to conf files. Default: .')
        parser.add_argument('-n', '--et_name', default='ET2', help='Set engineering team name')
        parser.add_argument('-f', '--file_name', default='envs.properties', help='Set name of file to save env vars')
        return parser

    parser = createParser()
    namespace = parser.parse_args()

    ### Set variables from CLI
    ET = namespace.et_name
    F_NAME = namespace.file_name
    CONF_DIR = namespace.directory

    MainRun = main(ET, CONF_DIR, F_NAME)

    for SERVICE in MainRun.GetSERVICELIST:
        MainRun.getServiceVars(SERVICE)
        MainRun.create_artifact_dict()
        MainRun.write_to_file(SERVICE)










