#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 14:27:41 2018

@author: nguyentran
"""
#from flask import Flask, request
#from flask_restful import Resource, Api, abort, reqparse
#import json
#from importlib import import_module
#import lib.rest_endpoints as rest_endpoints
#from detector_service_sample import DetectorService
#from collector_service_sample import CollectorService
#from storage_service_sample import StorageService
#from search_service_sample import SearchService
#from lib.resources import *
#import lib.serv_res_worker_mapping as mapping

from lib.component_service_builder import ComponentServiceBuilder
from importlib import import_module
from lib.conductor_meta_client import ConductorMetaClient
import os

if __name__ == "__main__":
    wf_server_addr_port = os.getenv('WF_SERVER', "127.0.0.1:8080")
    host_addr_port = os.getenv("HOST_ADDR_PORT", "http://127.0.0.1:5000")
    cs_builder = ComponentServiceBuilder()
    cs = cs_builder.build("config.json", conn_to_conductor=True, 
                          wf_server_addr_port = wf_server_addr_port, 
                          host_addr_port=host_addr_port)
#    cs = cs_builder.build("config.json", conn_to_conductor=False)
    cs.boot()