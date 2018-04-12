#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 14:40:47 2018

@author: nguyentran
"""
from abc import ABC, abstractmethod
from .conductor.ConductorWorker import ConductorWorker
import requests
import json

class AbsConductorClient(ABC):
    def __init__(self, host_addr, rest_endpoint, wf_server_addr, task_name = "", *args, **kwargs):
        """
        Conductor client polls a workflow server to new instance of a specific task
        that it handles. It invoke the service handling this task, and returns its
        output to the conductor server.
        
        host_addr = network address of the component service handling this task
        rest_endpoint = rest endpoint of the component service
        task_name = name of the task, as registered in the WF server
        wf_server_addr = IP address of the workflow server
        """
        self.host_addr = host_addr
        self.rest_endpoint = rest_endpoint
        if not task_name:
            self.task_name = ""
        else:
            self.task_name = task_name
        self.wf_server_addr = wf_server_addr
        
    def start_polling(self, num_threads = 1, polling_interval = 0.1, wait = False):
        """
        Hook handling function, which handles communicating with component services
        to the task and start polling.
        """
        cc = ConductorWorker(self.wf_server_addr, num_threads, polling_interval)
        cc.start(self.task_name, self._invoke_service, wait)

    def send_get_request(self, append_to_endpoint = "", cookies = {}):
        if type(cookies) is not dict:
            raise TypeError("cookies passed to send_get_request() must be a dictionary. Current type: %s" % type(cookies))
        r = requests.get("%s%s" % (self.host_addr, self.rest_endpoint + append_to_endpoint), cookies = cookies)
        result = r.json()
        return result
    
    def send_post_request(self, send_data = None, cookies = {}):
        """
        Assume that data is not a JSON string.
        This method dumps the given data into a JSON before sending over HTTP
        """
        if type(cookies) is not dict:
            raise TypeError("cookies passed to send_post_request() must be a dictionary. Current type: %s" % type(cookies))
        r = None
        if send_data is not None:
            r = requests.post("%s%s" % (self.host_addr, self.rest_endpoint), data = json.dumps(send_data), headers = {"content-type" : "application/json"}, cookies = cookies)
        else:
            r = requests.post("%s%s" % (self.host_addr, self.rest_endpoint), headers = {"content-type" : "application/json"}, cookies = cookies)
        print(str(r))
        print("%s%s" % (self.host_addr, self.rest_endpoint))
        result = r.json()
        print(result)
        return result
    
    def get_workflow_instance_id(self, task, wf_id_key = "workflowInstanceId"):
        return task[wf_id_key]
    
    def get_workflow_instance_cookie(self, task, wf_id_key = "workflowInstanceId"):
        wf_id = self.get_workflow_instance_id(task, wf_id_key = wf_id_key)
        return {"wf_id" : wf_id}
    
    @abstractmethod
    def _invoke_service(self, task):
        pass