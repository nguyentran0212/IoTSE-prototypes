#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 18:27:34 2018

@author: nguyentran
"""

from lib.abstract_services import AbsCollectorService
import time
import math
import lib.entity as entity

class SampleData():
    def __init__(self, *args, **kwargs):
        iot_content1 = entity.IoTContent("source 1", {"type" : "temp sensor"}, {"value" : 34})
        iot_content2 = entity.IoTContent("source 2", {"type" : "humidity sensor"}, {"value" : 54})
        iot_content3 = entity.IoTContent("source 3", {"type" : "light sensor"}, {"value" : 5})
        self.req_id = "123456"    
        self.data = {self.req_id : [iot_content1, iot_content2, iot_content3]}
        
sample_data = SampleData()

class CollectorService(AbsCollectorService):
    def _collect(self, urlList, wf_id = ""):
#        with open("test_cookie.txt", "a") as f:
#            f.write("From %s: %s\n" % (self, wf_id))
#        print(urlList)
#        return urlList
        return sample_data.req_id
    
    def _lookup(self, req_id, wf_id = ""):
        return sample_data.data[req_id]