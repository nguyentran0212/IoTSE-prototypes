#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 12:07:58 2018

@author: nguyentran

This module declares all available URL endpoints to be used by component services
"""


"""
new_res_ids endpoint is utilised by detector services

GET: get ids of available IoT content, detected by detector services
"""
new_res_ids = "/api/new-res-ids"



"""
res_contents endpoint is utilised by collector services

POST: collect content of IoT resources identified by a list of given URL. URL 
of a timestamped list of collected content is returned instead.
"""
res_contents = "/api/res-contents"



"""
res_content endpoint is utilised by collector services

GET: collect the timestamped set of IoT content directly from collector service
"""
res_content = "/api/res-contents/<timestamp>"



"""
resources endpoint is utilised by storage services

POST: collect a batch of IoT content from the given URL and add to the database
"""
resources = "/api/iot-resources"



"""
resource endpoint is utilised by storage services

GET: get a single IoT resource
"""
resource = "/api/iot-resources/<res_id>"



"""
queries endpoint is utilised by search services

POST: accept a query. Start the query processing process and return URL pointing
to a generated list of search results
"""
queries = "/api/queries"



"""
results endpoint is utilised by search services

GET: retrieve the list of search results matching the given id
"""
results = "/api/results/<result_id>"