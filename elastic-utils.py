#!/usr/bin/env python
#coding: utf_8

# Example:
# ./elastic_utils.py

import sys, argparse, os
import json
import datetime
import requests
import time


class Controller():

    """Requirements: pip install requests, argparse
    Run: 'python3 elastic-utils.py -h' for help.
    """
    def __init__(self):
        # Set Unbuffered stdout
        sys.stdout = Unbuffered(sys.stdout)

        # Set default variables
        self.elasticsearch_port = None
        self.elasticsearch_url = None
        self.mapping_json_list = None
        self.action = None

        # Parse CLI args and set variables
        self.CreateParser()
## curl -XPUT http://$ELASTICSEARCH_URL:9200/_template/profiles -H 'Content-Type: application/json' -d@/workdir/profiles.json

    def ParseJsonGetVersion(self):
        pass

    def GetTemplate(self):
        pass

    def ChooseAction(self):
        api = ElasticseachApi(self.elasticsearch_url, self.elasticsearch_port, self.mapping_json_list, self.action)
        if self.mapping_json_list and self.action == 'remove':
            for mapping in self.mapping_json_list:
                print("[{:%Y-%m-%d %H:%M:%S}]: ############# START TO WORK WITH Elasticseach #############: {}".format(datetime.datetime.now(), mapping))
                result = api.RemoveRequest(mapping)
                api.CheckResult(result)
        elif self.mapping_json_list and self.action == 'create':
            for mapping in self.mapping_json_list:
                print("[{:%Y-%m-%d %H:%M:%S}]: ############# START TO WORK WITH Elasticseach #############: {}".format(datetime.datetime.now(), mapping))
                result = api.CreateRequest(mapping)
                api.CheckResult(result)
        else:
            print("[{:%Y-%m-%d %H:%M:%S}]: ERROR: Action: --{}-- doesn't exist or manual mapping list is empty: --{}--".format(datetime.datetime.now(), self.action, self.mappings_names))

    def TransformToList(self, entity):
        # Check if var not list, and try to transform it
        if entity:
            try:
                transformed_data = [item for item in entity.split(',')]
                return transformed_data
            except AttributeError:
                try:
                    transformed_data = [item for item in entity.split(' ')]
                    return transformed_data
                except AttributeError:
                    return entity
        else:
            return ['']

    def CreateParser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-elastic', '--elastic_url', default='elastic-elasticsearch-client', help='Specify Elasticsearch client host')
        parser.add_argument('-p', '--elastic_port', default='9200', help='Specify Elasticsearch port')
        parser.add_argument('-m', '--mapping_json_list', default=[''] , help='Set list of json separated by space. Example: -d webpages.json posts.json')
        parser.add_argument('-a', '--action', required=True, help='Choose action to execute: remove, create')
        self.elasticsearch_url = parser.parse_args().elastic_url
        self.elasticsearch_port = parser.parse_args().elastic_port
        self.mapping_json_list = self.TransformToList(parser.parse_args().mapping_json_list)
        self.action = parser.parse_args().action


class ElasticseachApi():

    def __init__(self, elasticsearch_url, elasticsearch_port, mapping_json_list, action):

        self.apiTimeout = 60

        # It's impossible to create a few mappings at one's. getting 409 error
        # Concurrent config changing...
        self.timeout_between_execution = 5

        # Set variables:
        self.elasticsearch_port = elasticsearch_url
        self.elasticsearch_url = elasticsearch_port
        self.mapping_json_list = mapping_json_list
        self.action = action

        # Set Unbuffered stdout
        sys.stdout = Unbuffered(sys.stdout)


    def GetListRequest(self):
        pass

    def GetStatusRequest(self, mapping):
        pass

    def RemoveRequest(self, mapping):
        # Get name of current mapping in kafka (name + version).
        current_mapping = self.BeforeRemoveRequest(mapping)
        try:
            print('[{:%Y-%m-%d %H:%M:%S}]: INFO: Try to remove {} mapping'.format(datetime.datetime.now(), current_mapping))
            resp = requests.delete('http://{}:8083/mappings/{}'.format(self., current_mapping), timeout=self.apiTimeout)
            print('[{:%Y-%m-%d %H:%M:%S}]: INFO: {} mapping is removed'.format(datetime.datetime.now(), current_mapping))
            return resp
        except Exception as e:
            print("[{:%Y-%m-%d %H:%M:%S}]: ERROR: {}".format(datetime.datetime.now(), e))
            sys.exit(1)
            
    def CreateRequest(self, mapping):
        # Check if such mapping template exists return pair of mapping name and version.
        mapping_data = self.BeforeCreateRequest(mapping)

        mapping_file_name = mapping + ".json"
        workdir = os.path.dirname(sys.argv[0])  # Set current workdir

        # Increase version of mapping if such mapping exists
        if mapping_data: # Check if dict not empty
            print('[{:%Y-%m-%d %H:%M:%S}]: INFO: Increase version of {} mapping template'.format(datetime.datetime.now(), mapping))
            self.IncreseVersion(workdir, mapping_file_name, mapping, mapping_version=mapping_data[mapping])
        else:
            print('[{:%Y-%m-%d %H:%M:%S}]: INFO: Here is no need to increase version. Go ahead'.format(datetime.datetime.now(), mapping))

        with open('{}/{}'.format(workdir, mapping_file_name),'rb') as f:
            print('[{:%Y-%m-%d %H:%M:%S}]: INFO: Try to create {} mapping'.format(datetime.datetime.now(), mapping_file_name))
            resp = requests.post('http://{}:{}/_template/profiles'.format(self.elasticsearch_url, self.elasticsearch_port), data=f, headers={'Content-Type':'application/json'}, timeout=self.apiTimeout)
            print('[{:%Y-%m-%d %H:%M:%S}]: INFO: {} mapping is created. Wait {} seconds for applying configuration'.format(datetime.datetime.now(), mapping, self.timeout_between_execution))
            time.sleep(int('{}'.format(self.timeout_between_execution)))
        return resp


    def IncreseVersion(self, workdir, mapping_file_name, mapping, mapping_version):
        # Replace name of mapping to the same name and increase version
        with open('{}/{}'.format(workdir, mapping_file_name)) as f:
            newData = f.read().replace('{}-{}'.format(mapping,mapping_version), '{}-{}'.format(mapping, (int(mapping_version) + 1)))
        # Save and close
        with open('{}/{}'.format(workdir, mapping_file_name), "w") as f:
            f.write(newData)

    def BeforeCreateRequest(self, mapping):
        mappings_dict = self.getCurrentmappingsDict()

        if mappings_dict:             # Check if dict not empty
            try:
                if mappings_dict[mapping]:  # Check if mapping exists in dict
                    print("[{:%Y-%m-%d %H:%M:%S}]: INFO: Removing: {} at first.".format(datetime.datetime.now(), mapping))
                    self.removeRequest(mapping)
                    return {mapping:mappings_dict[mapping]}
            except KeyError:
                    print("[{:%Y-%m-%d %H:%M:%S}]: INFO: For now mapping: {} doesn't exist.".format(datetime.datetime.now(), mapping))
                    return {}



    def CheckResult(self, result):
        if str(result.status_code).startswith('2'):
            print('[{:%Y-%m-%d %H:%M:%S}]: INFO: REQUEST is OK. CODE: {}, TXT: {}'.format(datetime.datetime.now(), result.status_code, result.text))
        elif str(result.status_code) in ['404']:
            print('[{:%Y-%m-%d %H:%M:%S}]: WARN: List of given mappings are empty. CODE: {}, TXT: {}'.format(datetime.datetime.now(), result.status_code, result.text))
        elif str(result.status_code) in ['409']:
            print('[{:%Y-%m-%d %H:%M:%S}]: WARN: mapping already exists, try to remove... CODE: {}, TXT: {}'.format(datetime.datetime.now(), result.status_code, result.text))
        else:
            print("[{:%Y-%m-%d %H:%M:%S}]: ERROR: CODE: {}, TXT: {}".format(datetime.datetime.now(), result.status_code, result.text))
            sys.exit(1)


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

if __name__ == '__main__':
    # Initialize class
    run = Controller()
