#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 18:24:08 2018

@author: nguyentran
"""

from ..cs_kernel.abs_conductor_client import AbsConductorClient as AbsConductorClient

        
class SearcherConductorClient(AbsConductorClient):    
    
    def _invoke_service(self, task):
        send_data = task["inputData"]["iotse_msg"]
        result = self.send_post_request(send_data = send_data, cookies=self.get_workflow_instance_cookie(task))
        return {'status': 'COMPLETED', 'output': {"iotse_msg" : result}, 'logs' : []}