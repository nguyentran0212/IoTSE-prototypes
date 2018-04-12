#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 18:33:09 2018

@author: nguyentran
"""

from ..cs_kernel.base_builder import ComponentServiceBuilder as BaseBuilder
from . import resources
from . import conductor_client

class DetectorBuilder(BaseBuilder):
    def __init__(self, host_addr, rest_endpoint, wf_server_addr, detector_task_name = None, *args, **kwargs):
        if detector_task_name is None:
            """
            if a custom task name is given, use the custom name
            otherwise, use the default name
            """
            detector_task_name = "detect"
        super().__init__(host_addr, rest_endpoint, wf_server_addr, task_name = detector_task_name, )
    
    def __init__(self):
        mapping = {"detector" : 
            ([(resources.NewResIDsPost, "/api/new-cont-ids"), (resources.NewResIDsGet, "/api/new-cont-ids/<req_id>")],
    [(conductor_client.DetectorConductorClient, "/api/new-cont-ids")])}
        super().__init__(mapping)