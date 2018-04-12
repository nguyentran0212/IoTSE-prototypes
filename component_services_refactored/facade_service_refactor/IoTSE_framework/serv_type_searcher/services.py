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
        
class AbsSearcherService(AbsService):
    serv_type = "search"
    def __init__(self, *args, **kwargs):
        super().__init__(self.serv_type, *args, **kwargs)
        
    def query(self, query, wf_id = ""):
        """
        This function search the database to resolve the given query
        and put search result into a storage space, and return the identifier
        of that list of search results to the client
        """
        query_id = self._query(query, wf_id=wf_id)
        return query_id
        
    def getResult(self, query_id, wf_id = ""):
        """
        This function returns the set of results generated from a previous query
        """
        result_set = self._getResult(query_id, wf_id=wf_id)
        return result_set

    @abstractmethod
    def _query(self, query, wf_id = ""):
        pass
    
    @abstractmethod
    def _getResult(self, result_id, wf_id = ""):
        pass