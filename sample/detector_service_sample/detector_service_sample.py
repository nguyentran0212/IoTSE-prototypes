#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 18:06:56 2018

@author: nguyentran
"""

from lib.abstract_services import AbsDetectorService

class SampleData():
    def __init__(self):
        self.res_ids = ["http://gateway/res_1", "http://gateway/res_2", 
                        "http://gateway/res_3", "http://gateway/res_4"]
        
sample_data = SampleData()

class DetectorService(AbsDetectorService):
    def _detect(self, wf_id = ""):
#        with open("test_cookie.txt", "a") as f:
#            f.write("From %s: %s\n" % (self, wf_id))
        return sample_data.res_ids