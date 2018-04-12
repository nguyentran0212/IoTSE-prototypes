#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 16:44:47 2018

@author: nguyentran

IoTSE defines 3 types of entity:
    IoTContent: represent a named IoT content, encapsulating ID, metadata, and content
    Query: represent a named query, encapsulating query_ID, query_content (a dictionary)
    ResultSet: represent a named collection of IoT content - score tuples
"""

from ..cs_kernel.entity_base import Entity as Entity
import copy

class IoTContent(Entity):
    def __init__(self, ID = "", metadata = {}, content = {}, iot_content_dict = None):
        super().__init__()
        if iot_content_dict is not None:
            self.from_dict(iot_content_dict)
        else:
            self.ID = ID
            self.metadata = metadata
            self.content = content
    
    def from_dict(self, iot_content_dict):
        self.ID = iot_content_dict["ID"]
        self.metadata = iot_content_dict["metadata"]
        self.content = iot_content_dict["content"]
        
class Query(Entity):
    def __init__(self, query_ID = "", query_content = {}, query_dict = None):
        super().__init__()
        if query_dict is not None:
            self.from_dict(query_dict)
        else:
            self.query_ID = query_ID
            self.query_content = query_content
        
    def from_dict(self, query_dict):
        self.query_ID = query_dict["query_ID"]
        self.query_content = query_dict["query_content"]
        
class ResultSet(Entity):
    def __init__(self, query_ID = "", query_instance = {}, results = None, result_set_dict = None):
        super().__init__()
        if result_set_dict is not None:
            self.from_dict(result_set_dict)
        else:
            self.query_ID = query_ID
            if type(query_instance) is not dict and type(query_instance) is not Query:
                raise TypeError("query_instance must be either a dictionary or an instance of Query entity")
            if type(query_instance) is Query:
                query_instance = query_instance.to_dict()
            self.query_instance = query_instance
            if results is None:
                self.results = []
            else:
                self.results = results
        
    def add_IoTContent_score(self, IoTContent = {}, score = {}):
        self.results.append((IoTContent, score))
        
    def to_dict(self):
        temp_list = []
        for result in self.results:
            try:
                temp_list.append((result[0].to_dict(), result[1]))
            except AttributeError:
                return self.__dict__
        temp_obj = copy.copy(self)
        temp_obj.results = temp_list
        return temp_obj.__dict__
        
    def from_dict(self, result_set_dict):
        self.query_ID = result_set_dict["query_ID"]
        self.query_instance = result_set_dict["query_instance"]
        self.results = result_set_dict["results"]