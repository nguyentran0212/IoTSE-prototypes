#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 16:23:01 2018

@author: nguyentran

Web resource classes encapsulate the logic for handling and responding to HTTP requests
Abstract resource class in this module provides the foundation for designing
resource classes, which are utilised in different types of component services.
"""

from flask import Flask, request, abort
from flask_restful import Resource, Api, abort, reqparse
import yaml
import re

class AbsResource(Resource):
    def __init__(self, service = None, self_host_post = "", rest_endpoint = "",  *args, **kwargs):
        self.service = service
        self.rest_endpoint = rest_endpoint
        self.self_host_port = self_host_post
        
    #==========================================================================
    # utilities 
    #==========================================================================
    def create_parser(self, *args):   
        # Create a parser for form data submitted by clients via POST or PUT
        parser = reqparse.RequestParser()
        # Configure the parser to look for certain argument in the submitted data
        # Submitted data can be considered a dictionary with argument : value pairs
        # This is an argument
        for arg in args:
        # Indicate that this API expects an argument named task in the submitted data
        # After parsing, we can be sure the given argument exists and the data is safe
            parser.add_argument(arg)
        return parser
    
    def extract_from_payload(self, key, payload_key = "payload"):
        parser = self.create_parser(payload_key)
        args = parser.parse_args()
    
#        with open("simple_service_log.txt", "w") as file:
#            file.write(str(request.values))
#            file.write(str(messages.CollectorPostResMessage(request.url, 
#                                       "timestamp-id of the collected set of IoT content", 
#                                       contentURL).to_dict()))
        
        value = yaml.load(args[payload_key])[key]
        return value
    
    def extract_from_cookies(self, key = ""):
        value = request.cookies.get(key)
        return value
    
    def extract_workflow_id(self, wf_id = "wf_id", abort_req = False):
        """
        Extract workflow id from the cookie sent to this service
        """
        workflow_id = self.extract_from_cookies(key = wf_id)
        if workflow_id and type(workflow_id) is str:
            # If workflow id is available as a string, return as is
            return workflow_id
        else:
            if abort_req:
                # If abort flag is set, return error code and stop processing the request
                abort(400)
            else:
                # otherwise, return an empty string
                return ""
    
    def generate_host_port_endpoint(self, endpoint = None):
        """
        This utility remove <var> from endpoint, and create
        a complete URL pointing to a resource from host_port and endpoint
        
        if endpoint is not given, this function returns URL pointing to self
        """
        if endpoint is None:
            endpoint = self.rest_endpoint
        endpoint_proc = re.sub(r"<.*?>", "", endpoint)
        url = "%s%s" % (self.self_host_port, endpoint_proc)
        """
        Remove trailing /
        """
        url = re.sub(r"\/$", "", url)
        return url