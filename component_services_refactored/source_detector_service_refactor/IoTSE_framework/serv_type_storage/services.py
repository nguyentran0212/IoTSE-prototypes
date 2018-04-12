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
        
class AbsStorageService(AbsService):
    serv_type = "storage"
    def __init__(self, *args, **kwargs):
        super().__init__(self.serv_type, *args, **kwargs)
        
    def insert(self, iot_contents, wf_id = ""):
        """
        Retrieve set of resources at the targeted URL and insert them
        to the database
        """
        result = self._insert(iot_contents, wf_id=wf_id)
        return result
    
    def getSingleResource(self, res_id, wf_id = ""):
        """
        Get a single resource from the storage
        """
        result = self._getSingleResource(res_id, wf_id=wf_id)
        return result
        
    @abstractmethod
    def _insert(self, iot_contents, wf_id = ""):
        pass
    
    @abstractmethod
    def _getSingleResource(self, res_id, wf_id = ""):
        pass