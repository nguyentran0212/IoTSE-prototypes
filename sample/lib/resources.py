#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 12:33:00 2018

@author: nguyentran
"""

from flask import Flask, request, abort
from flask_restful import Resource, Api, abort, reqparse
import json
import yaml
from lib.abstract_services import *

import lib.messages as messages

class AbsResource(Resource):
    def __init__(self, service = None):
        self.service = service
        
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
    
        with open("simple_service_log.txt", "w") as file:
            file.write(str(request.values))
    #        file.write(str(messages.CollectorPostResMessage(request.url, 
    #                                   "timestamp-id of the collected set of IoT content", 
    #                                   contentURL).to_dict()))
        
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


#==================================
# /api/new-res-ids
#==================================
class NewResIDs(AbsResource):
    """
    This resource is served by detector services
    """
    def get(self):
        """
        GET request to this resource invoke the discovery process for IoT content
        
        After initial test, consider adding **kwarg
        """
        workflow_id = self.extract_workflow_id()
#        with open("test_cookie.txt", "a") as f:
#            f.write("From NewResIDs: %s \n" % workflow_id)
        res_ids = self.service.detect(wf_id = workflow_id)
        msg = messages.DetectorGetResMessage(request.url, "Invoked discovery process", res_ids, workflow_id = workflow_id)
        return msg.to_dict()

#==================================
# /api/res-contents & /api/res-contents/<timestamp>
#==================================
class ResContents(AbsResource):
    """
    This resource is served by collector services
    """
    def post(self):
        """
        Endpoint: /api/res-contents
        
        POST request to this resource invoke the collection process for IoT content
        at the given identifiers. Content is timestamped and store.
        Every new POST request replaces the previous timestamp with a newer one
        """
        workflow_id = self.extract_workflow_id()
#        with open("test_cookie.txt", "a") as f:
#            f.write("From ResContents: %s\n" % workflow_id)
            
        urlList = self.extract_from_payload("res_ids")
        
        contentURL = self.service.collect(urlList, request.host, wf_id = workflow_id)
#        with open("simple_service_log.txt", "w") as file:
#            file.write(str(urlList))
#            file.write(str(contentURL))
#            file.write(str(messages.CollectorPostResMessage(request.url, 
#                                       "timestamp-id of the collected set of IoT content", 
#                                       contentURL).to_dict()))
        msg = messages.CollectorPostResMessage(request.url, 
                                       "timestamp-id of the collected set of IoT content", 
                                       contentURL, workflow_id = workflow_id)
        return msg.to_dict() , 201

class ResContent(AbsResource):
    """
    This resource is served by collector services
    """
    def get(self, timestamp):
        """
        Endpoint: /api/res-contents/<time-stamp-id>
        
        GET request to this resource returns the set of collected IoT res
        """
        workflow_id = self.extract_workflow_id()
#        with open("test_cookie.txt", "a") as f:
#            f.write("From ResContent: %s\n" % workflow_id)
            
        contents = self.service.lookup(timestamp, wf_id = workflow_id)
        return messages.CollectorGetResMessage(request.url, "List of IoT content at the given timestamp", contents, workflow_id = workflow_id).to_dict()

#==================================
# /api/iot-resources & /api/iot-resources/<res_id>
#==================================
class Resources(AbsResource):
    """
    This resource is served by IoT resource storage
    """
    def post(self):
        
        workflow_id = self.extract_workflow_id()
#        with open("test_cookie.txt", "a") as f:
#            f.write("From Resources: %s\n" % workflow_id)
            
        # Get the url of data to retrieve
        res_contents_url = self.extract_from_payload("res_contents_url")
        
        # Get content from URl and add to the database
        self.service.insert(res_contents_url, wf_id = workflow_id)
        
        return messages.StoragePostResMessage(request.url, workflow_id = workflow_id).to_dict() , 201
    
class Res(AbsResource):
    """
    This resource is served by IoT resource storage. It represents individual 
    resource item
    """
    def get(self, res_id):
        """
        GET request to this resource returns an individual resource item in
        the storage
        """
        workflow_id = self.extract_workflow_id()
#        with open("test_cookie.txt", "a") as f:
#            f.write("From Res: %s\n" % workflow_id)
            
        return {"res" : self.service.getSingleResource(res_id, wf_id = workflow_id)}

#==================================
# /api/queries
#==================================
class Queries(AbsResource):
    """
    Served by a searcher service. It represents the set of all queries handled 
    by a searcher service
    """
    def post(self):
        """
        POST request to this resource sends a query and invoke the search process
        It returns URL of the newly created result resource corresponding to the incoming query
        """
        workflow_id = self.extract_workflow_id()
#        with open("test_cookie.txt", "a") as f:
#            f.write("From Queries: %s\n" % workflow_id)
            
        query = self.extract_from_payload("query")
        result_url = self.service.query(query, wf_id = workflow_id)
        return messages.SearcherPostQueryMessage(request.url, "Finished query. Find the result at the included URL", result_url, workflow_id = workflow_id).to_dict() , 201
    
#==================================
# /api/results
#==================================
class Result(AbsResource):
    """
    Served by a searcher service. It represents the set of all results generated
    by a searcher service
    """
    def get(self, result_id):
        """
        GET request to this resource returns an individual resource item in
        the storage
        """
        workflow_id = self.extract_workflow_id()
#        with open("test_cookie.txt", "a") as f:
#            f.write("From Result: %s\n" % workflow_id)
            
        results = self.service.getResult(result_id, wf_id = workflow_id)
        return messages.SearcherGetResultMessage(request.url, "Results", results, workflow_id = workflow_id).to_dict()
    
#==================================
# /queries
#==================================
class FacadeQueries(AbsResource):
    """
    Served by a facade service. It provides the entry point to the system for 
    search clients
    """
    def post(self):
        """
        POST request to this resource sends a query and invoke the search process
        It returns URL of the newly created result resource corresponding to the incoming query
        """
        
        
        workflow_id = self.extract_workflow_id()
            
        query = request.get_json(force=True)
        result_url = self.service.query(query, request.host, wf_id = workflow_id)
        msg = messages.FacadePostQueryMessage(request.url, "Finished query. Find the result at the included URL", result_url, workflow_id = workflow_id)
        return msg.to_dict() , 201
    
#==================================
# /results/<result_id>
#==================================
class FacadeResultGet(AbsResource):
    """
    Served by a facade service. It provides and endpoint for search clients
    to retrieve the status of their submitted queries
    """
    def get(self, result_id):
        """
        GET request to this resource check the current state of the given query
        and return the url of the server holding result list if it is available
        """
        workflow_id = self.extract_workflow_id()          
        result_url = self.service.getResult(result_id, wf_id = workflow_id)
        msg = messages.FacadeGetResultMessage(request.url, "Url of the result", result_url, workflow_id = workflow_id)
        return msg.to_dict()
    
#==================================
# /results
#==================================
class FacadeResultPost(AbsResource):
    """
    Served by a facade service. This endpoint accepts updates from other services
    to update the state of a query under processing
    """
    def post(self):
        """
        POST request to this resource to update the URL pointing to the result list
        of a processing query
        """
        workflow_id = self.extract_workflow_id(abort_req=True)
        result_url = self.extract_from_payload("result_url")
        msg_from_service = self.service.updateResult(workflow_id, result_url)
        msg = messages.FacadePostResultMessage(request.url, msg_from_service, workflow_id = workflow_id)
        return msg.to_dict()