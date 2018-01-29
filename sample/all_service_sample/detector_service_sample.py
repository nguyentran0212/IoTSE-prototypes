#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 18:06:56 2018

@author: nguyentran
"""

from lib.abstract_services import AbsDetectorService
import lib.entity as entity

class SampleData():
    def __init__(self):
        iot_content1 = entity.IoTContent("source 1", {"type" : "sensor source"}, {"url" : "http://gateway/res_1"})
        iot_content2 = entity.IoTContent("source 2", {"type" : "sensor source"}, {"url" : "http://gateway/res_2"})
        iot_content3 = entity.IoTContent("source 3", {"type" : "sensor source"}, {"url" : "http://gateway/res_3"})
        self.req_id = "123456"    
        self.data = {self.req_id : [iot_content1, iot_content2, iot_content3]}
    
sample_data = SampleData()

class DetectorService(AbsDetectorService):
    def _detect(self, iot_contents = [], wf_id = ""):
#        with open("test_cookie.txt", "a") as f:
#            f.write("From %s: %s\n" % (self, wf_id))
        return sample_data.req_id
    
    def get_detect_result(self, req_id = "", wf_id = ""):
        return sample_data.data[req_id]