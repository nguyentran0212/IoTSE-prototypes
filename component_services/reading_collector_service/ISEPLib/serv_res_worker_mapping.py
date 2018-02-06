#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 16:21:26 2018

@author: nguyentran
"""

from importlib import import_module
import ISEPLib.rest_endpoints as rest_endpoints
resource_module_name = "ISEPLib.resources"
conductor_clients_module_name = "ISEPLib.conductor_clients"

"""
Mapping between type of service, and the list of REST resources classes, rest_endpoints,
and conductor clients to use with this type of service

(resource_class, endpoint to attach resource to)
(conductor_client_class, endpoint to invoke when receiving task from WF server)
"""
mapping = {
        "detector" : ([("NewResIDsPost", rest_endpoints.new_res_ids_post), ("NewResIDsGet", rest_endpoints.new_res_ids_get)], [("DetectorConductorClient", rest_endpoints.new_res_ids_post)]),
        "collector" : ([("ResContentsPost", rest_endpoints.res_contents_post), ("ResContentsGet", rest_endpoints.res_contents_get)], [("CollectorConductorClient", rest_endpoints.res_contents_post)]),
        "storage" : ([("Contents", rest_endpoints.storage_contents_post_get)], [("StorageConductorClient", rest_endpoints.storage_contents_post_get)]),
        "search" : ([("Queries", rest_endpoints.queries), ("Result", rest_endpoints.results)], [("SearcherConductorClient", rest_endpoints.queries)]),
        "aggregator" : ([("AggregatorResultsPost", rest_endpoints.aggregate_results_post), ("AggregatorResultsGet", rest_endpoints.aggregate_results_get)], [("AggregatorAddResultConductorClient", rest_endpoints.aggregate_results_post)]),
        "facade" : ([("FacadeQueries", rest_endpoints.facade_queries), ("FacadeResultGet", rest_endpoints.facade_results_get), ("FacadeResultPost", rest_endpoints.facade_results_post)], [("FacadeConductorClient", rest_endpoints.facade_results_post)])        
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