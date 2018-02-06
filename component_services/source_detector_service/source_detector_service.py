#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 18:06:56 2018

@author: nguyentran
"""

from ISEPLib.abstract_services import AbsDetectorService
import ISEPLib.entity as entity

class DetectorService(AbsDetectorService):
    def __init__(self, wsp_host_port = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        iot_source = entity.IoTContent("wsr_1", {"type" : "sensor source"}, {"url" : wsp_host_port})
        self.sources = {"wsp" : [iot_source]}
    
    def _detect(self, iot_contents = [], wf_id = ""):
        """
        return a predefined key for client to retrieve the set of detected content later
        """
        return list(self.sources.keys())[0]
    
    def get_detect_result(self, req_id = "", wf_id = ""):
        """
        retrieve the list of IoT content sources
        """
        return self.sources.get(req_id, None)