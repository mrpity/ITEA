#!/usr/bin/env python
#coding: utf_8

import sys, json, argparse, httplib
import configparser
from xml.dom import minidom
import requests
import re
import operator


class main(TEAM, COMPONENT):

    def __init__(self, TEAM, COMPONENT):

        createParser(self, TEAM, COMPONENT)

        parser = createParser()
        namespace = parser.parse_args()

        ### Set variables from CLI
        self.ET = namespace.et_name
        self.SERVICE = namespace.service
        self.CONF_DIR = namespace.directory

    ### Parse CLI vars
    def createParser(self, TEAM, COMPONENT):
        parser = argparse.ArgumentParser()
        #    parser.add_argument('-n','--et_name', required=True, help='Set engineering team name: ET2, ET1')
        #    parser.add_argument('-s','--service', required=True, help='Set service type: CDS_BE, CDS_FE, CMS_BE, CMS_FE, WAS, OLA, RTA, TAS, DBS, CLIENT_LOCALE, ADMIN_LOCALE')
        parser.add_argument('-d', '--directory', default='.', help='Path to conf files. Default: .')
        parser.add_argument('-n', '--et_name', default='{}'.format(TEAM), help='Set engineering team name')
        parser.add_argument('-s', '--service', default='{}'.format(COMPONENT), help='Set service type')
        return parser

    parser = createParser()
    namespace = parser.parse_args()

    ### Set variables from CLI
    ET = namespace.et_name
    SERVICE = namespace.service
    CONF_DIR = namespace.directory

    def createConfVars(CONF_DIR, ET, SERVICE):

        ### Include conf file according to TYPE
        config = configparser.ConfigParser()
        conf_dir = '{}/{}.ini'.format(CONF_DIR ,ET)
        config.read(conf_dir)                          # include conf file in the same dir with main script. Default path: .

        ### Check if conf file exists and options in conf file exist
        try:
            GetCOMMON = config['COMMON']
        except Exception:
            print("ERROR. Cann't find config COMMON in file: {}. Maybe this file doesn't exist".format(conf_dir))

        ### Check if options in conf file exist
        try:
            GetService = config['{}'.format(SERVICE)]
        except KeyError, NameError:
            print ("ERROR. Service: {} doesn't exist".format(SERVICE))

        return [GetCOMMON, GetService]

    conf_vars = createConfVars(CONF_DIR, ET, SERVICE)

    def createArtifactoryVars(GetCOMMON, GetService):

        ### Set vars from conf file
        ARTIFACTORY = GetCOMMON['URL']
        SERVICE_REPO = GetService['SERVICE_REPO']
        SERVICE_ARTIFACT_ID = GetService['SERVICE_ARTIFACT_ID']
        SERVICE_GROUP_ID = GetService['SERVICE_GROUP_ID']
        return [ARTIFACTORY, SERVICE_REPO, SERVICE_GROUP_ID, SERVICE_ARTIFACT_ID]

    artifactory_vars = createArtifactoryVars(conf_vars[0], conf_vars[1])  # conf_vars[0] -- GetCOMMON from createConfVars

    def GetXML(ARTIFACTORY, SERVICE_REPO, SERVICE_GROUP_ID, SERVICE_ARTIFACT_ID):

        ### From direct link for meven-metadata.xml from artifactory
        artifactory_link = '{}/{}/{}/{}/maven-metadata.xml'.format(ARTIFACTORY,SERVICE_REPO,SERVICE_GROUP_ID,SERVICE_ARTIFACT_ID )
        addr = requests.get(artifactory_link)

        ### Raise exception if there is no access to maven-metadata.xml
        if addr.status_code != 200:
            print("ERROR.Cann't get access to {}, code status: {}".format(artifactory_link,addr.status_code))
            raise SystemExit(1)
        return addr

    addr = GetXML(artifactory_vars[0], artifactory_vars[1],artifactory_vars[2], artifactory_vars[3]) # artifactory_vars[0] --- ARTIFACTORY from createArtifactoryVars

    ### Create unique artifact list from field: 'version' from maven-metadata.xml that is mentioned above.
    def form_artifact_list(addr):
        maven_xml = minidom.parseString(addr.text)
        versions = maven_xml.getElementsByTagName("version")
        artifact_list = []
        for version in versions:
            artifact_list.append(version.childNodes[0].nodeValue)
        return set(artifact_list)

    artifact_list = form_artifact_list(addr)

    ### Create dict from unique artifact list for get the max/latest value from it
    RE='.*CI([0-9]+).*'    # Regular Expression. grep all versions like 3.9_cds-be_CI195-SNAPSHOT, 3.9_cds-be_CI204-SNAPSHOT
    def create_artifact_dict(list, RE):
        artifact_dict = {}
        for item in list:
            pattern_match = re.match(r'{}'.format(RE), item)
            if pattern_match:
                artifact_dict[pattern_match.group(1)] = item
        return artifact_dict

    artifact_dict = create_artifact_dict(artifact_list, RE)

    ### Get the latest artifact from dict that is mentioned above
    def get_latest_artifact(dict):
        latest_version = max(dict.iteritems(), key=operator.itemgetter(1))[0]
        latest_artifact = dict[latest_version]
        return latest_artifact

    latest_artifact = get_latest_artifact(artifact_dict)

    ### Check if var:latest_artifact isn't empty
    if not latest_artifact:
        print ("ERROR. latest_artifact var is empty: {}".format(latest_artifact))
        raise SystemExit(1)

    print latest_artifact

    ### Write latest_artifact to file. SERVICE_VER -- is needed var for ansible playbook
    def write_to_file(COMPONENT, latest_artifact):
        file_name = "vars_env.prorerties"
        f = open('{}'.format(file_name), 'a')
        f.write('{}={}\n'.format(COMPONENT, latest_artifact))
        f.close()

    write_to_file(COMPONENT, latest_artifact)



if __name__ == '__main__':


    pity = main('ET2', 'WAS')








