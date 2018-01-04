#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 18:06:56 2018

@author: nguyentran
"""

from abstract_services import AbsDetectorService

class SampleData():
    def __init__(self):
        self.res_ids = ["http://gateway/res_1", "http://gateway/res_2", 
                        "http://gateway/res_3", "http://gateway/res_4"]
        
sample_data = SampleData()

class DetectorService(AbsDetectorService):
    def _detect(self):
        return sample_data.res_ids