#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 12:09:15 2017

@author: nguyentran

This is a client for submitting definitions of workflows and tasks to a conductor server
The implementation is based on the python library included in the repository of netflix
"""

from conductor import conductor
from functools import wraps
import json
import argparse

WF_SERVER_PATH_DEFAULT = "http://localhost:8080/api"
#WF_SERVER_PATH_DEFAULT = "http://192.168.99.102:8080/api"

def getJSON(pathJSON):
    print(pathJSON)
    read_data = ""
    with open(pathJSON) as f:
        read_data = json.load(f)
    return read_data

def add_workflow(pathJSON, wf_server_path):
    wf_def = getJSON(pathJSON)
    metaClient = conductor.MetadataClient(wf_server_path)
    print(metaClient.createWorkflowDef(wf_def))
    print("Finish adding workflow at %s" % pathJSON)

def add_task(pathJSON, wf_server_path):
    task_def = getJSON(pathJSON)
    metaClient = conductor.MetadataClient(wf_server_path)
    print(metaClient.registerTaskDefs(task_def))
    print("Finish adding workflow at %s" % pathJSON)

def start_wf(wfName, inputjson, wf_server_path):
    wf_client = conductor.WorkflowClient(wf_server_path)
    wf_client.startWorkflow(wfName = wfName, inputjson = inputjson)
    print("Finish invoking workflow %s" % wfName)

# Output of a finished workout is stored in the description of the workflow instance
# This function retrieve representation of a workflow instance
def get_wf(wfId, wf_server_path):
    wf_client = conductor.WorkflowClient(wf_server_path)
    return wf_client.getWorkflow(wfId, includeTasks=False)
    


"""
Extract task path, wf path, and server path from the console
"""
parser = argparse.ArgumentParser(description="Tool for submitting task definitions, workflow definitions, and invoking workflows on a conductor workflow server")
parser.add_argument("wf_server_path", help="Address of conductor workflow server in form of http://url:8080/api")
parser.add_argument("task_path", help="Path to the json file storing declaration of tasks")
parser.add_argument("wf_path", help="Path to the json file storing declaration of workflows")
parser.add_argument("-s", "--start_wf_name", help= "Specify the name of a workflow to start immediately after declaration")
args = parser.parse_args()
wf_server_path = args.wf_server_path
task_def_path = args.task_path
wf_def_path = args.wf_path
wf_name_start = args.start_wf_name

print("Server path: %s" % wf_server_path)
print("Path to task definition json: %s" % task_def_path)
print("Path to workflow definition json: %s" % wf_def_path)
add_task(task_def_path, wf_server_path)
add_workflow(wf_def_path, wf_server_path)

if wf_name_start is not None:
    print("Name of workflow to start: %s" % wf_name_start)
    start_wf(wfName=wf_name_start, inputjson={})
    
#    start_wf(wfName = "iotse_prototype_interlaced", inputjson = {"iotse_msg" : "Hello to IoTSE, from the conductor", 
#                                                   "query" : {"payload" : {
#                                                           "query" : {
#                                                                   "type" : "temperature", 
#                                                                   "value" : "30"
#                                                                   }
#                                                           }}})
#    print(get_wf("128876b5-9d90-4eb0-b7f8-bbcf53e8beb5")["output"])