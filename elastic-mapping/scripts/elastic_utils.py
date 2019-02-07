#!/usr/bin/env python
#coding: utf_8

# Example:
# ./elastic_utils.py -a create -m webpages posts ...
# optional keys: -elastic: elasticsearch url,
#                -p: port,
#                -d: mapping_dir

import sys, argparse, os
import json
import datetime
import requests
import time
import pprint


class Controller():

    """Requirements: pip install requests, argparse, json
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
        # set directory from where we will read template mappings
        self.mappings_workdir = None

        # Parse CLI args and set variables
        self.CreateParser()
        #self.CreateParserLocal() # For local debug

    def ChooseAction(self):
        api = ElasticseachApi(self.elasticsearch_url, self.elasticsearch_port, self.mapping_json_list, self.action, self.mappings_workdir)
        if self.mapping_json_list and self.action == 'remove':
            for mapping in self.mapping_json_list:
                print("[{:%Y-%m-%d %H:%M:%S}]: ############# START TO WORK WITH ELASTICSEARCH TEMPLATE MAPPING: {} #############".format(datetime.datetime.now(), mapping))
                result = api.RemoveRequest(mapping)
                api.CheckResult(result)
        elif self.mapping_json_list and self.action == 'create':
            for mapping in self.mapping_json_list:
                print("[{:%Y-%m-%d %H:%M:%S}]: ############# START TO WORK WITH ELASTICSEARCH TEMPLATE MAPPING: {} #############".format(datetime.datetime.now(), mapping))
                result = api.CreateRequest(mapping)
                api.CheckResult(result)
        else:
            print("[{:%Y-%m-%d %H:%M:%S}]: ERROR: Action: --{}-- doesn't exist or manual mapping list is empty: --{}--".format(datetime.datetime.now(), self.action, self.mapping_json_list))

    def TransformToList(self, entity):
        # Check if 'entity' is not list, and try to transform it
        if entity:
            try:
                transformed_data = [item for item in entity[0].split(',')]
                return transformed_data
            except AttributeError:
                try:
                    transformed_data = [item for item in entity.split(' ')]
                    return transformed_data
                except AttributeError:
                    return entity
        else:
            print("[{:%Y-%m-%d %H:%M:%S}]: ERROR: Mapping list is empty: --{}--".format(datetime.datetime.now(), entity))
            sys.exit(1)

    def CreateParser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-e', '--elastic_url', default='elastic-elasticsearch-client', help='Specify Elasticsearch client host')
        parser.add_argument('-p', '--elastic_port', default='9200', help='Specify Elasticsearch port')
        parser.add_argument('-m', '--mapping_json_list', nargs='*', required=True, help='Set list of json separated by space. Example: -m webpages posts')
        parser.add_argument('-d', '--mapping_dir', default="/workdir", help='Set directory from where we will read template mappings')
        parser.add_argument('-a', '--action', required=True, help='Choose action to execute: remove, create')
        self.elasticsearch_url = parser.parse_args().elastic_url
        self.elasticsearch_port = parser.parse_args().elastic_port
        self.mapping_json_list = self.TransformToList(parser.parse_args().mapping_json_list)
        self.mappings_workdir = parser.parse_args().mapping_dir
        self.action = parser.parse_args().action


    def CreateParserLocal(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-e', '--elastic_url', default='localhost', help='Specify Elasticsearch client host')
        parser.add_argument('-p', '--elastic_port', default='9200', help='Specify Elasticsearch port')
        parser.add_argument('-m', '--mapping_json_list', nargs='*', required=True , help='Set list of json separated by space. Example: -d webpages posts.')
        parser.add_argument('-d', '--mapping_dir', default="../mappings", help='Set directory from where we will read template mappings')
        parser.add_argument('-a', '--action', default='remove', help='Choose action to execute: remove, create')
        self.elasticsearch_url = parser.parse_args().elastic_url
        self.elasticsearch_port = parser.parse_args().elastic_port
        self.mapping_json_list = self.TransformToList(parser.parse_args().mapping_json_list)
        self.mappings_workdir = parser.parse_args().mapping_dir
        self.action = parser.parse_args().action


class ElasticseachApi():

    def __init__(self, elasticsearch_url, elasticsearch_port, mapping_json_list, action, mappings_workdir):

        self.apiTimeout = 60

        # It's impossible to create a few mappings at one's. getting 409 error
        # Concurrent config changing...
        self.timeout_between_execution = 3

        # Set Unbuffered stdout
        sys.stdout = Unbuffered(sys.stdout)

        # Set variables:
        self.elasticsearch_port = elasticsearch_port
        self.elasticsearch_url = elasticsearch_url
        self.mapping_json_list = mapping_json_list
        self.action = action
        self.mappings_workdir = mappings_workdir

    def RemoveRequest(self, mapping):
        try:
            print('[{:%Y-%m-%d %H:%M:%S}]: INFO: Try to remove {} template mapping'.format(datetime.datetime.now(), mapping))
            resp = requests.delete('http://{}:{}/_template/{}'.format(self.elasticsearch_url, self.elasticsearch_port, mapping), timeout=self.apiTimeout)
            print('[{:%Y-%m-%d %H:%M:%S}]: INFO: {} template mapping is removing'.format(datetime.datetime.now(), mapping))
            return resp
        except Exception as e:
            print("[{:%Y-%m-%d %H:%M:%S}]: ERROR: {}".format(datetime.datetime.now(), e))
            sys.exit(1)
            
    def BeforeCreateRequest(self, mapping):
        # Set mapping file name and workdir
        mapping_file_name = self.AddJsonExpansion(mapping)  # Set full name of mapping file
        workdir = os.path.dirname(sys.argv[0]) + self.mappings_workdir # Set current workdir

        # Get version of mapping from file on local filesystem
        local_mapping_version = self.GetLocalJsonVersion(workdir, mapping)

        # Check if such mapping template exists in elasticsearch and return this version.
        remote_mapping_version = self.GetRemoteJsonVersion(mapping)

        # Check Remote and Local Versions
        print('[{:%Y-%m-%d %H:%M:%S}]: INFO: REMOTE VERSION: {} and LOCAL VERSION: {}'.format(datetime.datetime.now(),
                                                                                              remote_mapping_version,
                                                                                              local_mapping_version))
        self.CompareMappingsVersions(remote_mapping_version, local_mapping_version)

        return {'workdir':workdir, 'mapping_file_name':mapping_file_name}

    def CreateRequest(self, mapping):
        # Validate versions of mappings. Return workdir and file name
        file_mapping_info = self.BeforeCreateRequest(mapping)

        with open('{}/{}'.format(file_mapping_info['workdir'], file_mapping_info['mapping_file_name']),'rb') as f:
            print('[{:%Y-%m-%d %H:%M:%S}]: INFO: Try to create {} template mapping'.format(datetime.datetime.now(), file_mapping_info['mapping_file_name']))
            resp = requests.put('http://{}:{}/_template/{}'.format(self.elasticsearch_url, self.elasticsearch_port, mapping), data=f, headers={'Content-Type':'application/json'}, timeout=self.apiTimeout)
            print('[{:%Y-%m-%d %H:%M:%S}]: INFO: {} template mapping is creating. Wait {} seconds for applying configuration'.format(datetime.datetime.now(), mapping, self.timeout_between_execution))
            time.sleep(int('{}'.format(self.timeout_between_execution)))
        return resp

    def CompareMappingsVersions(self, remote_mapping_version, local_mapping_version):
        if remote_mapping_version is None:
            remote_mapping_version = 0
        if local_mapping_version is None:
            local_mapping_version = 0
        if local_mapping_version <= remote_mapping_version:
            print('[{:%Y-%m-%d %H:%M:%S}]: ERROR: Please increase current version({}) in local file, or remove this mapping from list for update procedure. And try again'.format(datetime.datetime.now(), local_mapping_version))
            sys.exit(1)
        print('[{:%Y-%m-%d %H:%M:%S}]: INFO: REMOTE VERSION: {} and LOCAL VERSION: {}'.format(datetime.datetime.now(),
                                                                                              remote_mapping_version,
                                                                                              local_mapping_version))

    def AddJsonExpansion(self, mapping):
        return mapping + ".json"

    def GetLocalJsonVersion(self, workdir, mapping):
        with open('{}/{}'.format(workdir, self.AddJsonExpansion(mapping)), "r") as f:
            try:
                json_object = json.load(f)
                print("[{:%Y-%m-%d %H:%M:%S}]: INFO: LOCAL: Try to get mapping version: {}".format(datetime.datetime.now(), mapping))
                return self.GetVersionFromJson(json_object, mapping)
            except Exception as e:
                print("[{:%Y-%m-%d %H:%M:%S}]: WARN: LOCAL: Could not serialize to json format: {}. It seems, mapping does not exist".format(datetime.datetime.now(), e))

    def GetRemoteJsonVersion(self, mapping):
        # Get full json data of mapping template
        resp = self.GetTemplateRequest(mapping)

        try:
            json_object = json.loads(resp.text)
            print("[{:%Y-%m-%d %H:%M:%S}]: INFO: REMOTE: Try to get mapping version: {}".format(datetime.datetime.now(), mapping))
            return self.GetVersionFromJson(json_object, mapping)
        except Exception as e:
            print("[{:%Y-%m-%d %H:%M:%S}]: WARN: REMOTE: Could not serialize to json format: {}. It seems, mapping does not exist".format(datetime.datetime.now(), e))

    def GetVersionFromJson(self, json_object, mapping):
        try:
            return json_object[mapping]['version']
        except Exception as e:
            print("[{:%Y-%m-%d %H:%M:%S}]: WARN: Could not get Version in json_object[{}]['version'].Try one more time".format(datetime.datetime.now(), mapping, e))
        try:
            return json_object['version']
        except Exception as e:
            print("[{:%Y-%m-%d %H:%M:%S}]: WARN: Could not get Version in json_object['version'] for {}. Try one more time".format(datetime.datetime.now(), mapping, e))

    def GetTemplateRequest(self, mapping):
        try:
            print('[{:%Y-%m-%d %H:%M:%S}]: INFO: REMOTE: Try to get {} mapping'.format(datetime.datetime.now(), mapping))
            resp = requests.get('http://{}:{}/_template/{}'.format(self.elasticsearch_url, self.elasticsearch_port, mapping), timeout=self.apiTimeout)
            return resp
        except Exception as e:
            print("[{:%Y-%m-%d %H:%M:%S}]: WARN: {}".format(datetime.datetime.now(), e))
            sys.exit(1)

    def CheckClusterHealth(self):
        pass

    def CheckResult(self, result):
        if str(result.status_code).startswith('2'):
            print('[{:%Y-%m-%d %H:%M:%S}]: INFO: REQUEST is OK. CODE: {}, TXT: {}'.format(datetime.datetime.now(), result.status_code, result.text))
        elif str(result.status_code) in ['404']:
            pprint.pprint('[{:%Y-%m-%d %H:%M:%S}]: WARN: Mapping does not exist. CODE: {}, TXT: {}'.format(datetime.datetime.now(), result.status_code, result.text))
        elif str(result.status_code) in ['409']:
            pprint.pprint('[{:%Y-%m-%d %H:%M:%S}]: WARN: Mapping already exists, try to remove... CODE: {}, TXT: {}'.format(datetime.datetime.now(), result.status_code, result.text))
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
    run.ChooseAction()
