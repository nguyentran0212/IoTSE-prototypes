#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 11:43:44 2017

@author: nguyentran

This module shows the client of a worker service. This client is a part of the worker service.
It is responsible for interacting with a conductor server.
When receive a new task, it invokes a corresponding function on the service
When the function finishes, it updates the task status to the conductor server
"""

from lib.conductor_clients import *
import lib.rest_endpoints as rest_endpoints

def main():
	# Start polling for task
    DetectorConductorClient("http://127.0.0.1:5000", rest_endpoints.new_res_ids).start_polling()
    CollectorConductorClient("http://127.0.0.1:5000", rest_endpoints.res_contents).start_polling()
    StorageConductorClient("http://127.0.0.1:5000", rest_endpoints.resources).start_polling()
    SearcherConductorClient("http://127.0.0.1:5000", rest_endpoints.queries).start_polling()
    FacadeConductorClient("http://127.0.0.1:5000", rest_endpoints.results).start_polling(wait=True)
    
if __name__ == '__main__':
    main()