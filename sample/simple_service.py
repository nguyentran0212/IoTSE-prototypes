#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 14:27:41 2018

@author: nguyentran
"""

from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
import json
import yaml
from abstract_services import *
from detector_service_sample import DetectorService
from collector_service_sample import CollectorService
from storage_service_sample import StorageService
from search_service_sample import SearchService
import messages
import rest_endpoints

app = Flask(__name__)
api = Api(app)



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
class NewResIDs(Resource):
    """
    This resource is served by detector services
    """
    def get(self):
        """
        GET request to this resource invoke the discovery process for IoT content
        
        After initial test, consider adding **kwarg
        """
        res_ids = DetectorService().detect()
        msg = messages.DetectorGetResMessage(request.url, "Invoked discovery process", res_ids)
        return msg.to_dict()

#==================================
# /api/res-contents & /api/res-contents/<timestamp>
#==================================
class ResContents(Resource):
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
        
        contentURL = CollectorService().collect(urlList, request.host)
        with open("simple_service_log.txt", "w") as file:
            file.write(str(urlList))
            file.write(str(contentURL))
            file.write(str(messages.CollectorPostResMessage(request.url, 
                                       "timestamp-id of the collected set of IoT content", 
                                       contentURL).to_dict()))
        return messages.CollectorPostResMessage(request.url, 
                                       "timestamp-id of the collected set of IoT content", 
                                       contentURL).to_dict() , 201

class ResContent(Resource):
    """
    This resource is served by collector services
    """
    def get(self, timestamp):
        """
        Endpoint: /api/res-contents/<time-stamp-id>
        
        GET request to this resource returns the set of collected IoT res
        """
        contents = CollectorService().lookup(timestamp)
        return messages.CollectorGetResMessage(request.url, "List of IoT content at the given timestamp", contents).to_dict()

#==================================
# /api/iot-resources & /api/iot-resources/<res_id>
#==================================
class Resources(Resource):
    """
    This resource is served by IoT resource storage
    """
    def post(self):
        # Get the url of data to retrieve
        res_contents_url = extract_from_payload("res_contents_url")
        
        # Get content from URl and add to the database
        StorageService().insert(res_contents_url)
        
        return messages.StoragePostResMessage(request.url).to_dict() , 201
    
class Res(Resource):
    """
    This resource is served by IoT resource storage. It represents individual 
    resource item
    """
    def get(self, res_id):
        """
        GET request to this resource returns an individual resource item in
        the storage
        """
        return {"res" : StorageService().getSingleResource(res_id)}

#==================================
# /api/queries
#==================================
class Queries(Resource):
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
        result_url = SearchService().query(query)
        return messages.SearcherPostQueryMessage(request.url, "Finished query. Find the result at the included URL", result_url).to_dict() , 201
    
#==================================
# /api/results
#==================================
class Result(Resource):
    """
    Served by a searcher service. It represents the set of all results generated
    by a searcher service
    """
    def get(self, result_id):
        """
        GET request to this resource returns an individual resource item in
        the storage
        """
        results = SearchService().getResult(result_id)
        return messages.SearcherGetResultMessage(request.url, "Results", results).to_dict()
    
# Connect resources to URL endpoints
api.add_resource(NewResIDs, rest_endpoints.new_res_ids)
api.add_resource(ResContents, rest_endpoints.res_contents)
api.add_resource(ResContent, rest_endpoints.res_content)
api.add_resource(Resources, rest_endpoints.resources)
api.add_resource(Res, rest_endpoints.resource)
api.add_resource(Queries, rest_endpoints.queries)
api.add_resource(Result, rest_endpoints.results)

if __name__ == "__main__":
    # It is CRITICAL to attach the server to the address 0.0.0.0 instead of the localhost. Otherwise, it cannot be accessed from the outside of a container
    app.run(debug=True, host="0.0.0.0")