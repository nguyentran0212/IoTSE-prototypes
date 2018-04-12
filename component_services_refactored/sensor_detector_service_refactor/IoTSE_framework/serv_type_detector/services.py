#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 17:10:54 2018

@author: nguyentran
"""

from ..cs_kernel.abs_service import AbsService as AbsService
from abc import abstractmethod

#import conductor_clients as conductor_clients
#import resources as resources

class AbsDetectorService(AbsService):
    serv_type = "detector"
    def __init__(self, *args, **kwargs):
        super().__init__(self.serv_type, *args, **kwargs)
    
    def detect(self, iot_contents = [], wf_id = ""):
        """
        This method detects URL of certain type of IoT resources and 
        return a unique id, allowing client to retrieve the result later
        
        If it encounters any error, it raises exceptions
        """
        
        req_id = self._detect(iot_contents = iot_contents, wf_id = wf_id)
        return req_id

    def get_detect_result(self, req_id = ""):
        return self._get_detect_result(req_id)

    @abstractmethod
    def _detect(self, iot_contents = [], wf_id = ""):
        """
        This method holds the implementation of detection algorithms offered by 
        component developers
        
        Expected output: list
        Input: N/A
        """
        pass
    
#    @abstractmethod
    def _get_detect_result(self, req_id = ""):
        """
        This method holds the implementation of retrieval of detection result
        matching the given req_id
        
        This method is OPTIONAL, thus it is not decorated with abstractmethod decorator
        """