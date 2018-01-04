#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 16:21:26 2018

@author: nguyentran
"""

from importlib import import_module
import lib.rest_endpoints as rest_endpoints
resource_module_name = "lib.resources"
conductor_clients_module_name = "lib.conductor_clients"

"""
Mapping between type of service, and the list of REST resources classes, rest_endpoints,
and conductor clients to use with this type of service

(resource_class, endpoint to attach resource to)
(conductor_client_class, endpoint to invoke when receiving task from WF server)
"""
mapping = {
        "detector" : ([("NewResIDs", rest_endpoints.new_res_ids)], [("DetectorConductorClient", rest_endpoints.new_res_ids)]),
        "collector" : ([("ResContents", rest_endpoints.res_contents), ("ResContent", rest_endpoints.res_content)], [("CollectorConductorClient", rest_endpoints.res_contents)]),
        "storage" : ([("Resources", rest_endpoints.resources), ("Res", rest_endpoints.resource)], [("StorageConductorClient", rest_endpoints.resources)]),
        "search" : ([("Queries", rest_endpoints.queries), ("Result", rest_endpoints.results)], [("SearcherConductorClient", rest_endpoints.queries), ("FacadeConductorClient", rest_endpoints.results)])        
        }

"""
Utility function to get resource classes relevant to the given type of service
"""
def get_resource_classes(key):
    resource_class_names = mapping[key][0]
    resources_module = import_module(resource_module_name)
    resource_classes = []
    for name, endpoint in resource_class_names:
        resource_classes.append((resources_module.__dict__[name], endpoint))
    return resource_classes

"""
Utility function to get conductor client classes relevant to the given type of service
"""    
def get_conductor_client_classes(key):
    conductor_client_class_names = mapping[key][1]
    conductor_client_module = import_module(conductor_clients_module_name)
    conductor_client_classes = []
    for name, endpoint in conductor_client_class_names:
        conductor_client_classes.append((conductor_client_module.__dict__[name], endpoint))
    return conductor_client_classes

if __name__ == "__main__":
    print(get_conductor_client_classes("detector"))