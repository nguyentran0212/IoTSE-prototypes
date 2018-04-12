#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 16:36:55 2018

@author: nguyentran
abs_IoTSE_resource extends the abs_resource class in the cs_kernel to add 
utilities specific for IoTSE. These utilities interact with entities types
defined by IoTSE, and therefore requires concrete knowledge of utilised
entity and message types.
"""

from ..cs_kernel.abs_resource import AbsResource as AbsResource
from ..IoTSE_models_messages import IoTSE_entities as entity
import requests

class AbsIoTSEResource(AbsResource):       
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