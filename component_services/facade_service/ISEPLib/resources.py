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
from ISEPLib.abstract_services import *
import requests
import re

import ISEPLib.message as message
import ISEPLib.entity as entity
import ISEPLib.rest_endpoints as rest_endpoints

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
    
        with open("simple_service_log.txt", "w") as file:
            file.write(str(request.values))
    #        file.write(str(messages.CollectorPostResMessage(request.url, 
    #                                   "timestamp-id of the collected set of IoT content", 
    #                                   contentURL).to_dict()))
        
        value = yaml.load(args[payload_key])[key]
        return value
    
    def extract_callback_url(self):
        """
        This method checks whether the given message is a callback message
        If it is the case, then extract the call back URL and return
        Otherwise, return "not_callback"
        """
        parser = self.create_parser("type")
        args = parser.parse_args()
       
        mes_type = args["type"]
        if mes_type == "callback_message":
            callback_url = self.extract_from_payload("url")
            return callback_url
        else:
            return "not_callback"
    
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
            
    def get_iot_contents(self, workflow_id = ""):
        """
        This utility helps getting iot contents, either from the received request,
        or from the callback url available in the request
        """
        callback_url = self.extract_callback_url()
        iot_contents = []
        if callback_url != "not_callback":
            """
            If the input message is a call back, send a request to 
            the callback link to get needed data
            """
            
            r = requests.get(callback_url, cookies = {"wf_id" : workflow_id})
            
            result = r.json()
            
            iot_content_dicts = result["payload"]["iot_contents"]
        else:
            """
            Otherwise, extract iot_contents from the request
            """
            iot_content_dicts = self.extract_from_payload("iot_contents")
            
        
        for iot_content_dict in iot_content_dicts:
                iot_contents.append(entity.IoTContent(iot_content_dict = iot_content_dict))
            
        return iot_contents
        
    def get_result_set(self, workflow_id = ""):
        """
        This utility helps getting a result set, either from the received request,
        or from the callback url available in the request
        """
        callback_url = self.extract_callback_url()
        result_set = None
        if callback_url != "not_callback":
            """
            If the input message is a call back, send a request to 
            the callback link to get needed data
            """
            
            r = requests.get(callback_url, cookies = {"wf_id" : workflow_id})
            
            result = r.json()
            
            result_set = result["payload"]["result_set"]
        else:
            """
            Otherwise, extract iot_contents from the request
            """
            result_set = self.extract_from_payload("result_set")
            
            
        return entity.ResultSet(result_set_dict=result_set)
    
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
    
    

#==================================
# /api/new-cont-ids
#==================================
class NewResIDsPost(AbsResource):
    """
    This resource is served by detector services.
    POST request to this resource starts the detection.
    Input: IoT Content entity (directly or via callback)
    Output: Callback message
    """    
    def post(self):
        """
        Get workflow id and inputs
        """
        workflow_id = self.extract_workflow_id()
        
        iot_contents = None
        try:
            iot_contents = self.get_iot_contents(workflow_id=workflow_id)
        except:
            """
            Do not abort the operation immediately because source detector does not
            need iot-content to work. Therefore, I leave the decision to 
            deal with non existence of iot content to the service implementation
            """
            print("Cannot find the iot content in either the message or at the call back")
            pass
        
        """
        Process and generate outputs
        """
        req_id = self.service.detect(iot_contents = iot_contents, wf_id = workflow_id)
        if req_id is None:
            """
            If we get a None request from the service, I assume that the client request is incorrect
            """
            abort(400)
        req_id = "%s/%s" % (self.generate_host_port_endpoint(), req_id)
        msg = message.CallbackMessage(request.url, "Invoked discovery process. Poll the returned URL for results.", req_id, workflow_id = workflow_id)
        return msg.to_dict(), 201

#==================================
# /api/new-cont-ids/<req_id>
#==================================
class NewResIDsGet(AbsResource):
    """
    This resource is served by detector services
    GET a list of resource IDs by a given key, which was generated by POST
    Input: N/A
    Output: IoT Content list message
    """
    def get(self, req_id):
        """
        Get workflow id and input key
        """
        workflow_id = self.extract_workflow_id()
        if req_id is None:
            abort(404)
            
        """
        Retrieve data and return 
        """
        res_ids = self.service.get_detect_result(req_id = req_id, wf_id = workflow_id)
        if res_ids is None:
            """
            If return from service is None, it means the given req_id is not available on this server
            """
            print("Resource %s does not exist." % req_id)
            abort(404)
        msg = message.IoTContentsMessage(request.url, "List of detected content id", res_ids, workflow_id = workflow_id) 
        return msg.to_dict()




#==================================
# /api/res-contents
#==================================
class ResContentsPost(AbsResource):
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

        # Get IoT content either directly from the message, or via call back        
        iot_contents = self.get_iot_contents(workflow_id=workflow_id)
        
        req_id = self.service.collect(iot_contents, request.host, wf_id = workflow_id)
        req_id = "%s/%s" % (self.generate_host_port_endpoint(), req_id)
        
        msg = message.CallbackMessage(request.url, "Invoked collection process. Poll the returned URL for results.", req_id, workflow_id = workflow_id)
        return msg.to_dict() , 201

#==================================
# /api/res-contents/<req_id>
#==================================
class ResContentsGet(AbsResource):
    """
    This resource is served by collector services
    """
    def get(self, req_id):
        workflow_id = self.extract_workflow_id()
#        with open("test_cookie.txt", "a") as f:
#            f.write("From ResContent: %s\n" % workflow_id)
            
        contents = self.service.lookup(req_id, wf_id = workflow_id)
        msg = message.IoTContentsMessage(request.url, "List of IoT content at the given req_id", contents, workflow_id = workflow_id)
        return msg.to_dict()




#==================================
# /api/iot-contents
#==================================
class Contents(AbsResource):
    """
    This resource is served by IoT resource storage
    """
    def post(self):
        
        workflow_id = self.extract_workflow_id()
            
        # Get IoT content either directly from the message, or via call back        
        iot_contents = self.get_iot_contents(workflow_id=workflow_id)
        
#        # Get the url of data to retrieve
#        res_contents_url = self.extract_from_payload("res_contents_url")
        
        # Get content from URl and add to the database
        self.service.insert(iot_contents, wf_id = workflow_id)
        
        url = self.generate_host_port_endpoint()
        msg = message.CallbackMessage(request.url, "Stored IoT content. Poll the returned URL for getting all stored IoT content.", url, workflow_id = workflow_id)
        
        return msg.to_dict(), 201 
    
#class Res(AbsResource):
#    """
#    This resource is served by IoT resource storage. It represents individual 
#    resource item
#    """
#    def get(self, res_id):
#        """
#        GET request to this resource returns an individual resource item in
#        the storage
#        """
#        workflow_id = self.extract_workflow_id()
##        with open("test_cookie.txt", "a") as f:
##            f.write("From Res: %s\n" % workflow_id)
#            
#        return {"res" : self.service.getSingleResource(res_id, wf_id = workflow_id)}




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
        query = self.extract_from_payload("query")
        query = entity.Query(query_dict=query)
        query_id = self.service.query(query, wf_id = workflow_id)
        result_url = "%s/%s" % (self.generate_host_port_endpoint(endpoint = rest_endpoints.results), query_id)
        msg = message.CallbackMessage(request.url, "Finished query. Find the result at the included URL", result_url, workflow_id = workflow_id)
        return msg.to_dict() , 201
    
#==================================
# /api/results
#==================================
class Result(AbsResource):
    """
    Served by a searcher service. It represents the set of all results generated
    by a searcher service
    """
    def get(self, query_id):
        """
        GET request to this resource returns an individual resource item in
        the storage
        """
        workflow_id = self.extract_workflow_id()
        result_set = self.service.getResult(query_id, wf_id = workflow_id)
        msg = message.ResultSetMessage(request.url, "Results", result_set, workflow_id = workflow_id)
        return msg.to_dict()
   

#==================================
# /api/results
#==================================
class AggregatorResultsPost(AbsResource):
    """
    Served by an aggregator service. It represents the set of all lists of search results
    submitted to the aggregator for aggregation
    """
    def post(self):
        """
        POST request to this resource sends a result URL and invoke the store process
        It returns URL to /api/results/<query_id> to retrieve aggregated results
        
        Expect a message in the format of SearcherPostQueryMessage
        """
        workflow_id = self.extract_workflow_id()
        result_set = self.get_result_set(workflow_id=workflow_id)
        query_id = self.service.store(result_set, wf_id = workflow_id)
        aggregated_result_url = "%s/%s" % (self.generate_host_port_endpoint(), query_id)
        msg = message.CallbackMessage(request.url, "Added result URL for the query %s. Find the result at the included URL" % (workflow_id), aggregated_result_url, workflow_id = workflow_id)
        return msg.to_dict() , 201
    
#==================================
# /api/results/<query_id>
#==================================
class AggregatorResultsGet(AbsResource):
    """
    Served by a searcher service. It represents the set of all results generated
    by a searcher service
    """
    def get(self, query_id):
        """
        GET request to this resource returns an individual resource item in
        the storage
        """
        workflow_id = self.extract_workflow_id()
        result_set = self.service.aggregate(query_id, wf_id = workflow_id)
        if type(result_set) is not entity.ResultSet:
            abort(404)
        msg = message.ResultSetMessage(request.url, "Aggregated Search Results", result_set, workflow_id = workflow_id)
        return msg.to_dict()
    
    
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
        query_content = request.get_json(force=True)
        query_id, workflow_id = self.service.query(query_content)
        result_url = "%s/%s" % (self.generate_host_port_endpoint(endpoint = rest_endpoints.facade_results_get), query_id)
        msg = message.CallbackMessage(request.url, "Finished query. Find the result at the included URL", result_url, workflow_id = workflow_id)

        return msg.to_dict() , 201
    
#==================================
# /results/<result_id>
#==================================
class FacadeResultGet(AbsResource):
    """
    Served by a facade service. It provides and endpoint for search clients
    to retrieve the status of their submitted queries
    """
    def get(self, query_id):
        """
        GET request to this resource check the current state of the given query
        and return the url of the server holding result list if it is available
        """
        workflow_id = self.extract_workflow_id()          
        result_set = self.service.getResult(query_id, wf_id = workflow_id)
        msg = None
        if type(result_set) is not entity.ResultSet:
            result_url = "%s/%s" % (self.generate_host_port_endpoint(), query_id)
            msg = message.CallbackMessage(request.url, "Result is not available. Please check again later.", result_url, workflow_id = workflow_id)
        else:
            msg = message.ResultSetMessage(request.url, "Results", result_set, workflow_id = workflow_id)
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
        workflow_id = self.extract_workflow_id()
        result_set = self.get_result_set(workflow_id=workflow_id)
        query_id = result_set.query_ID
        self.service.updateResult(query_id, result_set)
        result_url = "%s/%s" % (self.generate_host_port_endpoint(), query_id)
        msg = message.CallbackMessage(request.url, "Updated results of query %s" % query_id, result_url, workflow_id = workflow_id)
        return msg.to_dict(), 201