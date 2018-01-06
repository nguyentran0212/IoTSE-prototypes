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
#import conductor_clients as conductor_clients
#import resources as resources

class SampleData():
    def __init__(self):
        self.res_ids = ["http://gateway/res_1", "http://gateway/res_2", 
                        "http://gateway/res_3", "http://gateway/res_4"]
        
sample_data = SampleData()

class AbsService(ABC):
    def __init__(self, serv_type):
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
    def __init__(self):
        super().__init__(self.serv_type)
    
    def detect(self, wf_id = ""):
        """
        This method detects URL of certain type of IoT resources and return
        a list of detected URL.
        
        If it encounters any error, it raises exceptions
        """
        
        res_ids = self._detect(wf_id = wf_id)
        return res_ids

    @abstractmethod
    def _detect(self, wf_id = ""):
        """
        This method holds the implementation of detection algorithms offered by 
        component developers
        
        Expected output: list
        Input: N/A
        """
        pass

class AbsCollectorService(AbsService):
    serv_type = "collector"
    def __init__(self):
        super().__init__(self.serv_type)
    
    def collect(self, urlList, curr_host, wf_id = ""):
        result = self._collect(urlList, wf_id = wf_id)
        return "%s/api/res-contents/%s" % (curr_host, result)

    @abstractmethod
    def _collect(self, urlList, wf_id = ""):
        pass
        
    def lookup(self, timestamp, wf_id = ""):
        result = self._lookup(timestamp, wf_id=wf_id)
        return result
            
    @abstractmethod
    def _lookup(self, timestamp, wf_id = ""):
        pass

class AbsStorageService(AbsService):
    serv_type = "storage"
    def __init__(self):
        super().__init__(self.serv_type)
        
    def insert(self, res_contents_url, wf_id = ""):
        """
        Retrieve set of resources at the targeted URL and insert them
        to the database
        """
        result = self._insert(res_contents_url, wf_id=wf_id)
        return result
    
    def getSingleResource(self, res_id, wf_id = ""):
        """
        Get a single resource from the storage
        """
        result = self._getSingleResource(res_id, wf_id=wf_id)
        return result
        
    @abstractmethod
    def _insert(self, res_contents_url, wf_id = ""):
        pass
    
    @abstractmethod
    def _getSingleResource(self, res_id, wf_id = ""):
        pass

class AbsSearchService(AbsService):
    serv_type = "search"
    def __init__(self):
        super().__init__(self.serv_type)
        
    def query(self, query, wf_id = ""):
        """
        This function search the database to resolve the given query
        and put search result into a storage space, and return the identifier
        of that list of search results to the client
        """
        result = self._query(query, wf_id=wf_id)
        return result
        
    def getResult(self, result_id, wf_id = ""):
        """
        This function returns the set of results generated from a previous query
        """
        result = self._getResult(result_id, wf_id=wf_id)
        return result

    @abstractmethod
    def _query(self, query, wf_id = ""):
        pass
    
    @abstractmethod
    def _getResult(self, result_id, wf_id = ""):
        pass
