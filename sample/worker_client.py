#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 11:43:44 2017

@author: nguyentran

This module shows the client of a worker service. This client is a part of the worker service.
It is responsible for interacting with a conductor server.
When receive a new task, it invokes a corresponding function on the service
When the function finishes, it updates the task status to the conductor server
"""

from conductor.ConductorWorker import ConductorWorker
import requests
import json

def invoke_detector(task):
    r = requests.get("http://127.0.0.1:5000/api/new-res-ids")
    result = r.json()
    return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}

def invoke_collector(task):
    """
    Whenever pushing json through any kind of pipe, turn dictionary into JSON string first, using JSON dumps
    """
    r = requests.post("http://127.0.0.1:5000/api/res-contents", data = json.dumps(task["inputData"]["iotse_msg"]), headers = {"content-type" : "application/json"})
    result = r.json()
    return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}

def invoke_storage(task):
    r = requests.post("http://127.0.0.1:5000/api/iot-resources", data = json.dumps(task["inputData"]["iotse_msg"]), headers = {"content-type" : "application/json"})
    result = r.json()
    return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}

def invoke_searcher(task):
    r = requests.post("http://127.0.0.1:5000/api/queries", data = json.dumps(task["inputData"]["iotse_msg"]), headers = {"content-type" : "application/json"})
    result = r.json()
    return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}

def retrieve_results(task):
    """
    This might be called internally by the search engine facade instead of the conductor.
    Leave here for demonstration purpose
    """
    r = requests.get("http://127.0.0.1:5000/api/results/asdf")
    result = r.json()
    return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}


def main():
    print('Hello World')
    # Create a conductor worker client
    # Args: location of WF server, number of threads, and polling interval
    cc = ConductorWorker('http://localhost:8080/api', 1, 0.1)
	# Start polling for task
    cc.start('detect', invoke_detector, False)
    cc.start('collect', invoke_collector, False)
    cc.start('store', invoke_storage, False)
    cc.start('search', invoke_searcher, False)
    cc.start('get_result', retrieve_results, True)
    
if __name__ == '__main__':
    main()