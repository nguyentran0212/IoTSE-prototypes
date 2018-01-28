#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 14:41:49 2018

@author: nguyentran
"""

from lib.abstract_conductor_client import AbsConductorClient
import requests
        
class DetectorConductorClient(AbsConductorClient):
    def __init__(self, host_addr, rest_endpoint, wf_server_addr):
        super().__init__(host_addr, rest_endpoint, "detect", wf_server_addr)
        self.task_service_func = self.invoke_detector
    
    def invoke_detector(self, task):
        result = self.send_get_request(cookies=self.get_workflow_instance_cookie(task))
        return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}

class CollectorConductorClient(AbsConductorClient):
    def __init__(self, host_addr, rest_endpoint, wf_server_addr):
        super().__init__(host_addr, rest_endpoint, "collect", wf_server_addr)
        self.task_service_func = self.invoke_collector
    
    def invoke_collector(self, task):
        send_data = task["inputData"]["iotse_msg"]
        result = self.send_post_request(send_data, cookies=self.get_workflow_instance_cookie(task))
        return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}

class StorageConductorClient(AbsConductorClient):
    def __init__(self, host_addr, rest_endpoint, wf_server_addr):
        super().__init__(host_addr, rest_endpoint, "store", wf_server_addr)
        self.task_service_func = self.invoke_storage
    
    def invoke_storage(self, task):
        send_data = task["inputData"]["iotse_msg"]
        result = self.send_post_request(send_data, cookies=self.get_workflow_instance_cookie(task))
        return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}

class SearcherConductorClient(AbsConductorClient):
    def __init__(self, host_addr, rest_endpoint, wf_server_addr):
        super().__init__(host_addr, rest_endpoint, "search", wf_server_addr)
        self.task_service_func = self.invoke_searcher
    
    def invoke_searcher(self, task):
        send_data = task["inputData"]["iotse_msg"]
        result = self.send_post_request(send_data, cookies=self.get_workflow_instance_cookie(task))
        return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}

class AggregatorAddResultConductorClient(AbsConductorClient):
    def __init__(self, host_addr, rest_endpoint, wf_server_addr):
        super().__init__(host_addr, rest_endpoint, "add_result", wf_server_addr)
        self.task_service_func = self.invoke_aggregator
    
    def invoke_aggregator(self, task):
        send_data = task["inputData"]["iotse_msg"]
        result = self.send_post_request(send_data, cookies=self.get_workflow_instance_cookie(task))
        return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}
    
class AggregatorAggregateConductorClient(AbsConductorClient):
    def __init__(self, host_addr, rest_endpoint, wf_server_addr):
        super().__init__(host_addr, rest_endpoint, "aggregate", wf_server_addr)
        self.task_service_func = self.invoke_aggregator
    
    def invoke_aggregator(self, task):
        send_data = task["inputData"]["iotse_msg"]
        result = self.send_get_request(append_to_endpoint = "/%s" % self.get_workflow_instance_cookie(task)["wf_id"], cookies=self.get_workflow_instance_cookie(task))
        return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}

class FacadeConductorClient(AbsConductorClient):
    """
    This client is intended for facade service, which is under construction
    """
    def __init__(self, host_addr, rest_endpoint, wf_server_addr):
        super().__init__(host_addr, rest_endpoint, "get_result", wf_server_addr)
        self.task_service_func = self.invoke_facade_service
    
    def invoke_facade_service(self, task):
        send_data = task["inputData"]["iotse_msg"]
        result = self.send_post_request(send_data, cookies=self.get_workflow_instance_cookie(task))
        return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}