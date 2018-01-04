#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 12:33:00 2018

@author: nguyentran
"""

from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
import json
import yaml
from lib.abstract_services import *

import lib.messages as messages

#==========================================================================
# utilities 
#==========================================================================
def create_parser(*args):   
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

def extract_from_payload(key, payload_key = "payload"):
    parser = create_parser(payload_key)
    args = parser.parse_args()

    with open("simple_service_log.txt", "w") as file:
        file.write(str(request.values))
#        file.write(str(messages.CollectorPostResMessage(request.url, 
#                                   "timestamp-id of the collected set of IoT content", 
#                                   contentURL).to_dict()))
    
    value = yaml.load(args[payload_key])[key]
    return value

#==================================
# /api/new-res-ids
#==================================
class AbsResource(Resource):
    def __init__(self, service = None):
        self.service = service

class NewResIDs(AbsResource):
    """
    This resource is served by detector services
    """
    def get(self):
        """
        GET request to this resource invoke the discovery process for IoT content
        
        After initial test, consider adding **kwarg
        """
        res_ids = self.service.detect()
        msg = messages.DetectorGetResMessage(request.url, "Invoked discovery process", res_ids)
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

        urlList = extract_from_payload("res_ids")
        
        contentURL = self.service.collect(urlList, request.host)
        with open("simple_service_log.txt", "w") as file:
            file.write(str(urlList))
            file.write(str(contentURL))
            file.write(str(messages.CollectorPostResMessage(request.url, 
                                       "timestamp-id of the collected set of IoT content", 
                                       contentURL).to_dict()))
        return messages.CollectorPostResMessage(request.url, 
                                       "timestamp-id of the collected set of IoT content", 
                                       contentURL).to_dict() , 201

class ResContent(AbsResource):
    """
    This resource is served by collector services
    """
    def get(self, timestamp):
        """
        Endpoint: /api/res-contents/<time-stamp-id>
        
        GET request to this resource returns the set of collected IoT res
        """
        contents = self.service.lookup(timestamp)
        return messages.CollectorGetResMessage(request.url, "List of IoT content at the given timestamp", contents).to_dict()

#==================================
# /api/iot-resources & /api/iot-resources/<res_id>
#==================================
class Resources(AbsResource):
    """
    This resource is served by IoT resource storage
    """
    def post(self):
        # Get the url of data to retrieve
        res_contents_url = extract_from_payload("res_contents_url")
        
        # Get content from URl and add to the database
        self.service.insert(res_contents_url)
        
        return messages.StoragePostResMessage(request.url).to_dict() , 201
    
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
        return {"res" : self.service.getSingleResource(res_id)}

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
        query = extract_from_payload("query")
        result_url = self.service.query(query)
        return messages.SearcherPostQueryMessage(request.url, "Finished query. Find the result at the included URL", result_url).to_dict() , 201
    
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
        results = self.service.getResult(result_id)
        return messages.SearcherGetResultMessage(request.url, "Results", results).to_dict()