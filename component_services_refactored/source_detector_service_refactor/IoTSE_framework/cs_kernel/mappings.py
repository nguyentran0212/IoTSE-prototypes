#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 17:26:36 2018

@author: nguyentran
Mapping class encapsulates a set of (Resource class - URL endpoint) and (Conductor Client class - URL endpoint),
along with utilities to perform lookup by class name
"""

from importlib import import_module

"""
Mapping between type of service, and the list of REST resources classes, rest_endpoints,
and conductor clients to use with this type of service

Pattern:
(resource_class, endpoint to attach resource to)
(conductor_client_class, endpoint to invoke when receiving task from WF server)

Sample:
   mapping = {
        "detector" : ([(Resource.NewResIDsPost, rest_endpoints.new_res_ids_post), (Resource.NewResIDsGet, rest_endpoints.new_res_ids_get)], [(ConductorClients.DetectorConductorClient, rest_endpoints.new_res_ids_post)]),
        "collector" : ...,
        "storage" : ...,
        "search" : ...,
        "aggregator" : ...,
        "facade" : ...        
        } 
"""

class Mapping:
    def __init__(self, mapping):
        self.mapping = mapping

    """
    Utility function to get resource classes relevant to the given type of service
    """
    def get_resource_classes(self, key):
        return self.mapping[key][0]
    
    """
    Utility function to get conductor client classes relevant to the given type of service
    """    
    def get_conductor_client_classes(self, key):
        return self.mapping[key][1]
