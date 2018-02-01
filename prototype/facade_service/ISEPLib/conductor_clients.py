#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 14:41:49 2018

@author: nguyentran
"""

from ISEPLib.abstract_conductor_client import AbsConductorClient
import requests
        
class DetectorConductorClient(AbsConductorClient):
    def __init__(self, host_addr, rest_endpoint, wf_server_addr, detector_task_name = None, *args, **kwargs):
        if detector_task_name is None:
            """
            if a custom task name is given, use the custom name
            otherwise, use the default name
            """
            detector_task_name = "detect"
        super().__init__(host_addr, rest_endpoint, detector_task_name, wf_server_addr)
        self.task_service_func = self.invoke_detector
    
    def invoke_detector(self, task):
        send_data = task["inputData"]["iotse_msg"]
        result = self.send_post_request(send_data = send_data, cookies=self.get_workflow_instance_cookie(task))
        return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}

class CollectorConductorClient(AbsConductorClient):
    def __init__(self, host_addr, rest_endpoint, wf_server_addr, collector_task_name = None, *args, **kwargs):
        if collector_task_name is None:
            """
            if a custom task name is given, use the custom name
            otherwise, use the default name
            """
            collector_task_name = "collect"
        super().__init__(host_addr, rest_endpoint, collector_task_name, wf_server_addr)
        self.task_service_func = self.invoke_collector
    
    def invoke_collector(self, task):
        send_data = task["inputData"]["iotse_msg"]
        result = self.send_post_request(send_data, cookies=self.get_workflow_instance_cookie(task))
        return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}

class StorageConductorClient(AbsConductorClient):
    def __init__(self, host_addr, rest_endpoint, wf_server_addr, storage_task_name = None, *args, **kwargs):
        if storage_task_name is None:
            """
            if a custom task name is given, use the custom name
            otherwise, use the default name
            """
            storage_task_name = "store"
        super().__init__(host_addr, rest_endpoint, storage_task_name, wf_server_addr)
        self.task_service_func = self.invoke_storage
    
    def invoke_storage(self, task):
        send_data = task["inputData"]["iotse_msg"]
        result = self.send_post_request(send_data, cookies=self.get_workflow_instance_cookie(task))
        return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}

class SearcherConductorClient(AbsConductorClient):
    def __init__(self, host_addr, rest_endpoint, wf_server_addr, searcher_task_name = None, *args, **kwargs):
        if searcher_task_name is None:
            """
            if a custom task name is given, use the custom name
            otherwise, use the default name
            """
            searcher_task_name = "search"
        super().__init__(host_addr, rest_endpoint, searcher_task_name, wf_server_addr)
        self.task_service_func = self.invoke_searcher
    
    def invoke_searcher(self, task):
        send_data = task["inputData"]["iotse_msg"]
        result = self.send_post_request(send_data, cookies=self.get_workflow_instance_cookie(task))
        return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}

class AggregatorAddResultConductorClient(AbsConductorClient):
    def __init__(self, host_addr, rest_endpoint, wf_server_addr, agg_add_result_task_name = None, *args, **kwargs):
        if agg_add_result_task_name is None:
            """
            if a custom task name is given, use the custom name
            otherwise, use the default name
            """
            agg_add_result_task_name = "add_result"
        super().__init__(host_addr, rest_endpoint, agg_add_result_task_name, wf_server_addr)
        self.task_service_func = self.invoke_aggregator
    
    def invoke_aggregator(self, task):
        send_data = task["inputData"]["iotse_msg"]
        result = self.send_post_request(send_data, cookies=self.get_workflow_instance_cookie(task))
        return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}
    
class AggregatorAggregateConductorClient(AbsConductorClient):
    def __init__(self, host_addr, rest_endpoint, wf_server_addr, agg_aggregate_task_name = None, *args, **kwargs):
        if agg_aggregate_task_name is None:
            """
            if a custom task name is given, use the custom name
            otherwise, use the default name
            """
            agg_aggregate_task_name = "aggregate"
        super().__init__(host_addr, rest_endpoint, agg_aggregate_task_name, wf_server_addr)
        self.task_service_func = self.invoke_aggregator
    
    def invoke_aggregator(self, task):
        send_data = task["inputData"]["iotse_msg"]
        result = self.send_get_request(append_to_endpoint = "/%s" % self.get_workflow_instance_cookie(task)["wf_id"], cookies=self.get_workflow_instance_cookie(task))
        return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}

class FacadeConductorClient(AbsConductorClient):
    """
    This client is intended for facade service, which is under construction
    """
    def __init__(self, host_addr, rest_endpoint, wf_server_addr, facade_task_name = None, *args, **kwargs):
        if facade_task_name is None:
            """
            if a custom task name is given, use the custom name
            otherwise, use the default name
            """
            facade_task_name = "get_aggregated_result"
        super().__init__(host_addr, rest_endpoint, "get_aggregated_result", wf_server_addr)
        self.task_service_func = self.invoke_facade_service
    
    def invoke_facade_service(self, task):
        send_data = task["inputData"]["iotse_msg"]
        result = self.send_post_request(send_data, cookies=self.get_workflow_instance_cookie(task))
        return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}