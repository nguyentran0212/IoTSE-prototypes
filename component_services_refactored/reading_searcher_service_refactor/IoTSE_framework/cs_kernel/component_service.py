#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 17:15:00 2018

@author: nguyentran

ComponentService class represent a composite service, ready to be containerised
and started. It comprises the Web server and the orchestration client. Objects
of this class are created by an external builder
"""

from flask import Flask
from flask_restful import Api
from .mappings import Mapping as Mapping

class ComponentService:
    def __init__(self, self_host_port, wf_host_port, mapping, flask_listen_host = "0.0.0.0"):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        # Flask host denotes the interface on which Flask listens
        self.flask_listen_host = flask_listen_host
        # host is the IP address of the host serving this component service
        self.self_host_port = self_host_port
        self.wf_host_port = "http://%s/api" % wf_host_port
        self.conductor_worker_clients = []
        # IMPORTANT: require name of resource and conductor client modules
        self.mapping = Mapping(mapping)
        
    def add_resource_to_api(self, serv_type, serv, env_vars):
        """
        Use the mapping to get resource class and rest endpoint serving by 
        the given service, and add those resources to the api
        """
        class_and_endpoints = self.mapping.get_resource_classes(serv_type)
        for item in class_and_endpoints:
            self.api.add_resource(item[0], item[1], resource_class_kwargs = {"service" : serv, "self_host_post" : self.self_host_port, "rest_endpoint" : item[1]})
        
    def add_conductor_worker_clients(self, serv_type, env_vars):
        """
        env_vars might contain alternative task_name for conductor client
        it is unpacked using ** to pass to constructor of conductor clients
        """
        class_and_endpoints = self.mapping.get_conductor_client_classes(serv_type)
        for item in class_and_endpoints:
            """
            create a new worker client and append to the list maintained by the service component
            """
            self.conductor_worker_clients.append(item[0](self.self_host_port, item[1], self.wf_host_port, **env_vars))
        
    def start_polling(self, wait = False):
        for client in self.conductor_worker_clients:
            client.start_polling(wait = wait)
        
    def run(self, debug = True):
        self.app.run(debug = debug, host = self.flask_listen_host)
        
    def boot(self, run = False):
        self.start_polling()
        if run:
            self.run()