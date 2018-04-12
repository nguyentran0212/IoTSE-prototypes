#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 17:08:15 2018

@author: nguyentran
This module provides the base class for implementing service classes, which
encapsulate the interaction between the web service implementation 
and the component logic implemented by a component developer
"""

from abc import ABC


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