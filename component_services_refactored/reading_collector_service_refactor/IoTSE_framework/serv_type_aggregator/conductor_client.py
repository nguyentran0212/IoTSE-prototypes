#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 18:24:08 2018

@author: nguyentran
"""

from ..cs_kernel.abs_conductor_client import AbsConductorClient as AbsConductorClient
    

class AggregatorAddResultConductorClient(AbsConductorClient):
    def __init__(self, host_addr, rest_endpoint, wf_server_addr, agg_add_result_task_name = None, *args, **kwargs):
        if agg_add_result_task_name is None:
            """
            if a custom task name is given, use the custom name
            otherwise, use the default name
            """
            agg_add_result_task_name = "add_result"
        super().__init__(host_addr, rest_endpoint, wf_server_addr, task_name = agg_add_result_task_name)
    
    def _invoke_service(self, task):
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
        super().__init__(host_addr, rest_endpoint, wf_server_addr, task_name = agg_aggregate_task_name)
    
    def _invoke_service(self, task):
        send_data = task["inputData"]["iotse_msg"]
        result = self.send_get_request(append_to_endpoint = "/%s" % self.get_workflow_instance_cookie(task)["wf_id"], cookies=self.get_workflow_instance_cookie(task))
        return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}