#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 17:22:50 2018

@author: nguyentran

This module contains abstract classes of four types of services available in
an IoTSE instance:
    AbsDetectorService
    AbsCollectorService
    AbsStorageService
    AbsSearcherService
"""
from abc import ABC, abstractmethod
import ISEPLib.entity as entity
import ISEPLib.message as message
#import conductor_clients as conductor_clients
#import resources as resources

class SampleData():
    def __init__(self):
        self.res_ids = ["http://gateway/res_1", "http://gateway/res_2", 
                        "http://gateway/res_3", "http://gateway/res_4"]
        
sample_data = SampleData()

class AbsService(ABC):
    def __init__(self, serv_type, *args, **kwargs):
        self.serv_type = serv_type

#    def _check_type(self, method_name, var, var_type, in_var = False, var_name = ""):
#        if var is None or type(var) is not var_type:
#            error_msg = ""
#            if in_var:
#                error_msg = "Invalid input parameter type: The parameter %s of method %s accept only %s. Current type is %s. %s" % (var_name, method_name, var_type, type(var), var)
#            else:
#                error_msg = "Invalid return type: The %s method must return a %s. Current type is %s." % (method_name, var_type, type(var))
#            raise TypeError(error_msg)

#    def _invoke_method(self, method_name, in_args, out_args = []):
#        """
#        Check the input of the named method, invoke it, and check it output
#        return its output
#        
#        in_args = [(var_1, var_1_name, var_1_type), (var_2, var_2_name, var_2_type), ...]
#        out_args = [var_1_type, var_2_type, ...]
#        
#        DUE TO THE BUG OCCURING WHEN INVOKED METHOD RETURN MULTIPLE OUTPUTS,
#        OUTPUT CHECK IS HALTED
#        """
#        
#        def get(self, method_name):
#            """
#            Utility method for getting the function object of this instance by name
#            """
#            def func_not_found():
#                raise LookupError("Cannot find the method %s" % method_name)
#
#            method = getattr(self,method_name,func_not_found) 
#            return method
#        
#        # Check the type of in_args to ensure that it is a dictionary
#        self._check_type("_invoke_method", in_args, list, in_var=True, var_name="in_args")
#        
#        # Check the type of out_args to ensure that it is a dictionary of 2d tuple
#        self._check_type("_invoke_method", out_args, list, in_var=True, var_name="out_args")
#        
#        # Check the type of method name to ensure that it is a string
#        self._check_type("_invoke_method", method_name, str, in_var=True, var_name="method_name")
#        
#        # Get the method
#        method = get(self, method_name)
#        
#        # Bug here
#        # Check each input
#        for in_arg in in_args:
#            self._check_type(method_name, in_arg[0], in_arg[2], in_var=True, var_name=in_arg[1])
#            
#        # Unpack and invoke method
#        results = method(*[x[0] for x in in_args])
##        print(results)
##        # Check each output
##        for out_arg_type in out_args:
##            for result in results:
##                self._check_type(method_name, result, out_arg_type)
#        
#        return results

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
    
    def _get_detect_result(self, req_id = ""):
        """
        This method holds the implementation of retrieval of detection result
        matching the given req_id
        """
        

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