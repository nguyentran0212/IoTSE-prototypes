#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 12:22:54 2018

@author: nguyentran

wf_bootstrap utility reads declaration of tasks, event handlers, and workflows;
and submits them to a conductor engine according to instructions in a YAML document
"""
from conductor import conductor
import json
import yaml
import argparse
import os

class WFBootstrap:
    def __init__(self, instr_loc):
        with open(instr_loc, "r") as f:
            instr = yaml.load(f)
            self.wf_server = instr["wf_server"]
            self.task_def = instr["task_def"]
            try:
                self.event_handler_def = instr["event_handler_def"]
            except KeyError:
                self.event_handler_def = None
            self.wf_def = instr["wf_def"]
            
        
    def getJSON(self, pathJSON):
#        print(pathJSON)
        read_data = ""
        with open(pathJSON) as f:
            read_data = json.load(f)
        return read_data
        
    def add_workflow(self, pathJSON, wf_server_path):
        wf_def = self.getJSON(pathJSON)
        wf_name = wf_def["name"]
        metaClient = conductor.MetadataClient(wf_server_path)
        print(metaClient.createWorkflowDef(wf_def))
        print("--Finish adding the workflow %s defined in %s" % (wf_name, pathJSON))
        return wf_name
    
    def add_task(self, pathJSON, wf_server_path):
        task_def = self.getJSON(pathJSON)
        metaClient = conductor.MetadataClient(wf_server_path)
        print(metaClient.registerTaskDefs(task_def))
        print("--Finish adding tasks at defined in %s" % pathJSON)
    
    def add_event_handler(self, pathJSON, wf_server_path):
        event_handler_def = self.getJSON(pathJSON)
        eventClient = conductor.BaseClient(wf_server_path, "event")
        url = eventClient.makeUrl("")
        print(eventClient.post(url, None, event_handler_def))
        print("--Finish adding event handler at defined in %s" % pathJSON)
    
    def start_wf(self, wfName, inputjson, wf_server_path):
        wf_client = conductor.WorkflowClient(wf_server_path)
        wf_client.startWorkflow(wfName = wfName, inputjson = inputjson)
        print("--Finish invoking workflow %s" % wfName)
        
    def bootstrap(self):
        # Printing information of the wf server
        wf_server_path = self.wf_server["address"]
        print("##### Address of the Workflow Enginer Server: %s" % wf_server_path)
        
        # Submit task descriptions
        task_pathJSON = self.task_def["file"]
        print("##### Adding tasks from the declaration at %s" % task_pathJSON)
        self.add_task(task_pathJSON, wf_server_path)
        
        # Submit event handler description
        # Skip if this information is missing
        if self.event_handler_def:
            eh_pathJSON = self.event_handler_def["file"]
            print("##### Adding event handler from the declaration at %s" % eh_pathJSON)
            self.add_event_handler(eh_pathJSON, wf_server_path)
        
        # Submit definition and optionally start workflows
        for wf in self.wf_def:
            wf_pathJSON = wf["file"]
            start = wf["start"]
            print("##### Adding a workflow from the declaration at %s" % wf_pathJSON)
            wf_name = self.add_workflow(wf_pathJSON, wf_server_path)
            if start:
                self.start_wf(wf_name, {}, wf_server_path)
        
if __name__ == "__main__": 
    """
    Extract task path, wf path, and server path from the console
    """
    parser = argparse.ArgumentParser(description="Tool for submitting task definitions, workflow definitions, and invoking workflows on a conductor workflow server. It reads instructions from a YAML file")
    parser.add_argument("instr_path", help="Address of the YAML file containing orchestration instructions")
    args = parser.parse_args()
    instr_path = args.instr_path
    
    wf_bootstrap = WFBootstrap(instr_path)
    wf_bootstrap.bootstrap()
    
