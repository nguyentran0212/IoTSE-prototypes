#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 14:40:47 2018

@author: nguyentran
"""

from conductor.ConductorWorker import ConductorWorker
import requests
import json

class AbsConductorClient:
    def __init__(self, host_addr, rest_endpoint, task_name, wf_server_addr = "http://127.0.0.1:8080/api"):
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
        self.task_name = task_name
        self.task_service_func = None
        self.wf_server_addr = wf_server_addr
        
    def start_polling(self, num_threads = 1, polling_interval = 0.1, wait = False):
        """
        Hook handling function, which handles communicating with component services
        to the task and start polling.
        """
        cc = ConductorWorker(self.wf_server_addr, num_threads, polling_interval)
        cc.start(self.task_name, self.task_service_func, wait)

    def send_get_request(self):
        r = requests.get("%s%s" % (self.host_addr, self.rest_endpoint))
        result = r.json()
        return result
    
    def send_post_request(self, send_data):
        """
        Assume that data is not a JSON string.
        This method dumps the given data into a JSON before sending over HTTP
        """
        r = requests.post("%s%s" % (self.host_addr, self.rest_endpoint), data = json.dumps(send_data), headers = {"content-type" : "application/json"})
        result = r.json()
        return result