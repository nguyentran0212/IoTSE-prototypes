#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 12:07:58 2018

@author: nguyentran

This module declares all available URL endpoints to be used by component services
"""


"""
Endpoints of detector services
new_res_ids_post: for initialising the content detection process. Return <req_id>
new_res_ids_get: for getting results of content detection process. Return IoTContentsMessage
"""
new_res_ids_post = "/api/new-cont-ids"
new_res_ids_get = "/api/new-cont-ids/<req_id>"




"""
Endpoints of collector services
res_contents_post: for initisalising the content collection process. Return <req_id>
res_contents_get: for getting results of the collection process. Return 
"""
res_contents_post = "/api/res-contents"
res_contents_get = "/api/res-contents/<req_id>"



"""
Endpoint of storage services
storage_contents_post_get: for adding new iot-content to the storage. Return <storage_contents_get>.
  also for getting all content in the storage. Accept either callback or IoTContent message
storage_content_get: get a single content [NOT IMPLEMENTED]
"""
storage_contents_post_get="/api/iot-contents"




"""
Endpoint of searcher services
queries: post here to submit a new query to start query. Accept a query message. Return a callback message
    pointing to /api/results/<query_id>
results: retrieve the list of search results matching <query_id>. Return a result set message
"""
queries = "/api/queries"
results = "/api/results/<query_id>"




"""
Endpoint of aggregator service

aggregate_results_post: accept either a result set or a callback URL pointing to a result set. Return a callback message
aggregate with <query_id>
aggregate_results_get: Return a result set message
"""
aggregate_results_post = "/api/agg_results"
aggregate_results_get = "/api/agg_results/<query_id>"




"""
Endpoint of facade service
facade_queries: POST: accept a query object to start query processing. Each query is considered a standalone instance.
    Return a callback message. Internally, the facade service invokes query process workflow
facade_results_post: update result sets of a given query. Receives either a reult set or a callback message.
    Return a callback message pointing to facade_results_get
facade_results_get: Return a result set message
"""
facade_queries = "/queries"
facade_results_post = "/results"
facade_results_get = "/results/<query_id>"