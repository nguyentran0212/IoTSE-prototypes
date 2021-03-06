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

from ISEPLib.component_service_builder import ComponentServiceBuilder
from importlib import import_module
from ISEPLib.conductor_meta_client import ConductorMetaClient

#if __name__ == "__main__":
#    cs_builder = ComponentServiceBuilder()
##    cs = cs_builder.build("config.json", conn_to_conductor=True)
#    cs = cs_builder.build("config.json", conn_to_conductor=False)
#    cs.boot()

cs_builder = ComponentServiceBuilder()
#    cs = cs_builder.build("config.json", conn_to_conductor=True)
cs = cs_builder.build("config.json", conn_to_conductor=False)
cs.boot()
app = cs.app
app.run()