#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 18:27:34 2018

@author: nguyentran
"""

from abstract_services import AbsCollectorService
import time
import math

class SampleData():
    def __init__(self):
        self.res_ids = ["http://gateway/res_1", "http://gateway/res_2", 
                        "http://gateway/res_3", "http://gateway/res_4"]
        self.iot_contents = [{"res_id": "res1", "type" : "sensor", "status" : "down"},
                             {"res_id": "res2", "type" : "actuator", "status" : "down"},
                             {"res_id": "res3", "type" : "sensor", "status" : "up"}]
        
sample_data = SampleData()

class CollectorService(AbsCollectorService):
    def _collect(self, urlList):
        return math.floor(time.time())
    
    def _lookup(self, timestamp):
        return sample_data.iot_contents