#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 18:28:51 2018

@author: nguyentran
"""

from ISEPLib.abstract_services import AbsFacadeService
from ISEPLib.conductor_meta_client import ConductorMetaClient
import uuid
import redis
import pickle
import ISEPLib.entity as entity

class SimpleFacadeService(AbsFacadeService):
    """
    Simple implementation of facade service, utilising an in-memory dictionary 
    to store the mapping between workflow ids and result URLs
    """
    def __init__(self, search_workflow_name = "iotse_sample", wf_host_port = "http://127.0.0.1:8080/api", redis_host = "localhost", redis_port = 6379, redis_db = 0, *args, **kwargs):
        super().__init__(search_workflow_name, *args, **kwargs)
        wf_server_path = "http://%s/api" % wf_host_port
        self.meta_client = ConductorMetaClient(wf_server_path = wf_server_path)
        self.redis_client = redis.StrictRedis(host = redis_host, port = redis_port, db = redis_db)
        self.redis_query_id_key = "facade:query_id:"
    
    def _start_workflow(self, query):
        """
        Start a search workflow, and return the workflow instance id
        """
        wf_id = self.meta_client.start_wf(self.search_workflow_name, query)
        return wf_id
    
    def _add_query_id_to_lookup(self, query_id):
        """
        Add wf_id into a lookup data structure for future reference
        """
        self.redis_client.set(self.redis_query_id_key + query_id, None)
    
    def _retrieve_query_id_from_lookup(self, query_id):
        """
        Retrieve wf_id and result_url from a lookup data structure
        """
        p_result_set = self.redis_client.get(self.redis_query_id_key + query_id)
        result_set = pickle.loads(p_result_set)
        return result_set
        
    
    def _update_query_id_in_lookup(self, query_id, result_set):
        """
        Update the result_url at the given wf_id
        """
        p_result_set = pickle.dumps(result_set)
        self.redis_client.set(self.redis_query_id_key + query_id, p_result_set)
        
    def _generateQueryID(self):
        """
        Generate a unique ID for a query
        """
        return str(uuid.uuid4())
    
#    def getResult(self, result_id, wf_id = ""):
#        """
#        This function returns the set of results generated from a previous query
#        """
#        result_url = self._retrieve_wf_id_from_lookup(result_id)
#        if result_url == "":
#            result_url = "Not available. Please check later."
#        return result_url
