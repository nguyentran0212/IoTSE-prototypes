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
        
class AbsCollectorService(AbsService):
    serv_type = "collector"
    def __init__(self, *args, **kwargs):
        super().__init__(self.serv_type, *args, **kwargs)
    
    def collect(self, iot_contents, curr_host, wf_id = ""):
        urlList = []
        for iot_content in iot_contents:
            urlList.append(iot_content.content["url"])
        req_id = self._collect(urlList, wf_id = wf_id)
        return req_id

    @abstractmethod
    def _collect(self, urlList, wf_id = ""):
        pass
        
    def lookup(self, req_id, wf_id = ""):
        result = self._lookup(req_id, wf_id=wf_id)
        return result
            
    @abstractmethod
    def _lookup(self, req_id, wf_id = ""):
        pass