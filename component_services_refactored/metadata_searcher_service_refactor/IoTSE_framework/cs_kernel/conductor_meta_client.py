#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 20:02:44 2018

@author: nguyentran
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 12:09:15 2017

@author: nguyentran

This is a client for submitting definitions of workflows and tasks to a conductor server
The implementation is based on the python library included in the repository of netflix
"""

from .conductor import conductor
import json

class ConductorMetaClient:
    def __init__(self, wf_server_path = "http://localhost:8080/api"):
        self.wf_server_path = wf_server_path

    def getJSON(self, pathJSON):
        print(pathJSON)
        read_data = ""
        with open(pathJSON) as f:
            read_data = json.load(f)
        return read_data
    
    def add_workflow(self, pathJSON):
        wf_def = self.getJSON(pathJSON)
        metaClient = conductor.MetadataClient(self.wf_server_path)
        print(metaClient.createWorkflowDef(wf_def))
        print("Finish adding workflow at %s" % pathJSON)
    
    def add_task(self, pathJSON):
        task_def = self.getJSON(pathJSON)
        metaClient = conductor.MetadataClient(self.wf_server_path)
        print(metaClient.registerTaskDefs(task_def))
        print("Finish adding workflow at %s" % pathJSON)
    
    def start_wf(self, wfName, inputjson):
        wf_client = conductor.WorkflowClient(self.wf_server_path)
        wf_id = wf_client.startWorkflow(wfName = wfName, inputjson = inputjson)
#        print("Finish invoking workflow %s" % wfName)
        return wf_id

    
    # Output of a finished workout is stored in the description of the workflow instance
    # This function retrieve representation of a workflow instance
    def get_wf(self, wfId):
        wf_client = conductor.WorkflowClient(self.wf_server_path)
        return wf_client.getWorkflow(wfId, includeTasks=False)