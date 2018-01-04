#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 14:27:41 2018

@author: nguyentran
"""
from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
import lib.rest_endpoints as rest_endpoints
from detector_service_sample import DetectorService
from collector_service_sample import CollectorService
from storage_service_sample import StorageService
from search_service_sample import SearchService
from lib.resources import *
import lib.serv_res_worker_mapping as mapping

class ComponentService:
    def __init__(self, host, flask_host = "0.0.0.0"):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.flask_host = flask_host
        self.host = host
        self.conductor_worker_clients = []
        
    def add_resource_to_api(self, serv_type, serv):
        """
        Use the mapping to get resource class and rest endpoint serving by 
        the given service, and add those resources to the api
        """
        class_and_endpoints = mapping.get_resource_classes(serv_type)
        for item in class_and_endpoints:
            self.api.add_resource(item[0], item[1], resource_class_kwargs = {"service" : serv})
        
    def add_conductor_worker_clients(self, serv_type):
        class_and_endpoints = mapping.get_conductor_client_classes(serv_type)
        for item in class_and_endpoints:
            """
            create a new worker client and append to the list maintained by the service component
            """
            self.conductor_worker_clients.append(item[0](self.host, item[1]))
        
    def start_polling(self, wait = False):
        for client in self.conductor_worker_clients:
            client.start_polling(wait = wait)
        
    def run(self, debug = True):
        self.app.run(debug = debug, host = self.flask_host)
        
    def boot(self):
        self.start_polling()
        self.run()

class ComponentServiceBuilder:
    def build(self, services, host_addr_port = "http://127.0.0.1:5000"):
        """
        Build an instance of component service based on the given list of component services
        to include
        """
        cs = ComponentService(host_addr_port)
        for service in services:
            cs.add_resource_to_api(service.serv_type, service)
            cs.add_conductor_worker_clients(service.serv_type)
        return cs


if __name__ == "__main__":

    detector_service = DetectorService()
    collector_service = CollectorService()
    storage_service = StorageService()
    search_service = SearchService()
    
    cs = ComponentServiceBuilder().build([detector_service, collector_service, storage_service, search_service])
    cs.boot()