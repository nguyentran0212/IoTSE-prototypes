#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 17:10:54 2018

@author: nguyentran
"""

from ..cs_kernel.abs_service import AbsService as AbsService
from abc import abstractmethod
from ..IoTSE_models_messages import IoTSE_entities as entity
from ..IoTSE_models_messages import IoTSE_messages as message
        
class AbsFacadeService(AbsService):
    serv_type = "facade"
    def __init__(self, search_workflow_name, *args, **kwargs):
        super().__init__(self.serv_type, *args, **kwargs)
        self.search_workflow_name = search_workflow_name
        
    def query(self, query_content, wf_id = ""):
        """
        This function starts the query processing workflow,
        retrieve workflow id, create a lookup dictionary between workflow_id
        and url of the result, and generate a url for client to check
        the status of the query
        """
    #    start_wf(wfName = "iotse_sample", inputjson = {"iotse_msg" : "Hello to IoTSE, from the conductor", 
    #                                                   "query" : {"payload" : {
    #                                                           "query" : {
    #                                                                   "type" : "temperature", 
    #                                                                   "value" : "30"
    #                                                                   }
    #                                                           }}})
        query_ID = self._generateQueryID()
        query = entity.Query(query_ID = query_ID, query_content = query_content)
        msg = message.QueryMessage("facade-service", "Start the workflow with attached query", query = query)
        wf_id = self._start_workflow({"iotse_msg" : msg.to_dict()})
        self._add_query_id_to_lookup(query_ID)
        return query_ID, wf_id
    
    @abstractmethod
    def _start_workflow(self):
        """
        Start a search workflow, and return the workflow instance id
        """
        pass
    
    @abstractmethod
    def _add_query_id_to_lookup(self, query_id):
        """
        Add wf_id into a lookup data structure for future reference
        """
        pass
    
    @abstractmethod
    def _retrieve_query_id_from_lookup(self, query_id):
        """
        Retrieve wf_id and result_url from a lookup data structure
        """
        pass
    
    @abstractmethod
    def _update_query_id_in_lookup(self, query_id, result_set):
        """
        Update the result_url at the given wf_id
        """
        pass
    
    @abstractmethod
    def _generateQueryID(self):
        """
        Generate a unique ID for a query
        """
        pass
    
    def getResult(self, query_id, wf_id = ""):
        """
        This function returns the set of results generated from a previous query
        """
        result_set = self._retrieve_query_id_from_lookup(query_id)
        if result_set is None:
            result_set = "Not available. Please check later."
        return result_set

    def updateResult(self, query_id, result_set):
        self._update_query_id_in_lookup(query_id, result_set)
        return "Finish updating status of the query %s" % query_id