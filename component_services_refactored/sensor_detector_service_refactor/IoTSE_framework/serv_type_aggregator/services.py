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
        
class AbsAggregatorService(AbsService):
    serv_type = "aggregator"
    def __init__(self, *args, **kwargs):
        super().__init__(self.serv_type, *args, **kwargs)
        
    def store(self, result_set, wf_id = ""):
        """
        This function store the given URL of a result set to the internal
        storage for retrieval and aggregate in the future
        """
        query_id = self._store(result_set, wf_id=wf_id)
        return query_id
        
    def aggregate(self, query_id, wf_id = ""):
        """
        This function extract result sets from the database linking to the 
        given query_id, and perform the aggregation
        """
        result = self._aggregate(query_id, wf_id=wf_id)
        return result

    @abstractmethod
    def _store(self, result_url, wf_id = ""):
        pass
    
    @abstractmethod
    def _aggregate(self, query_id, wf_id = ""):
        pass