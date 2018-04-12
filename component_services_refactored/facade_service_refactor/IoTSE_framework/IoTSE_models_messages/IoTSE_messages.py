#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 16:44:55 2018

@author: nguyentran

IoTSE defines 4 types of messages:
    IoTContentsMessage: containing a list of IoT content objects in payload
    QueryMessage: containing a query object in payload
    ResultSetMessage: containing a result set object in payload
    CallbackMessage: containing URL for calling back to retrieve data in payload
"""

from ..cs_kernel.message_base import Message as Message
from . import IoTSE_entities as entity
    
class IoTContentsMessage(Message):
    """
    This message contains a list of instances of IoT content entity class
    """
    msg_type = "IoTContent_message"
    def __init__(self, sender, msg, iot_contents, workflow_id = ""):
        super().__init__(self.msg_type, sender, msg, workflow_id = workflow_id)
        if type(iot_contents) is not list:
            raise TypeError("iot_contents must a be a list of entity.IoTContent type")
        content_list = []
        for iot_content in iot_contents:
            if type(iot_content) is not entity.IoTContent:
                raise TypeError("iot_contents must a be a list of entity.IoTContent type")
            content_list.append(iot_content.to_dict())
        self._add_payload("iot_contents", content_list)
        
class QueryMessage(Message):
    """
    This message contains an instance of the Query entity class
    """
    msg_type = "query_message"
    def __init__(self, sender, msg, query, workflow_id = ""):
        super().__init__(self.msg_type, sender, msg, workflow_id = workflow_id)
        if type(query) is not entity.Query:
            raise TypeError("query must be an instance of entity.Query type")
        self._add_payload("query", query.to_dict())
        
class ResultSetMessage(Message):
    """
    This message contains an instance of the ResultSet entity class
    """
    msg_type = "result_set_message"
    def __init__(self, sender, msg, result_set, workflow_id = ""):
        super().__init__(self.msg_type, sender, msg, workflow_id = workflow_id)
        if type(result_set) is not entity.ResultSet:
            raise TypeError("result_set must be an instance of entity.ResultSet type")
        self._add_payload("result_set", result_set.to_dict())
        
class CallbackMessage(Message):
    """
    This message contains a URL for calling back to retrieve data of any kind
    """
    msg_type = "callback_message"
    def __init__(self, sender, msg, url, workflow_id = ""):
        super().__init__(self.msg_type, sender, msg, workflow_id = workflow_id)
        if type(url) is not str:
            raise TypeError("url must be a string")
        self._add_payload("url", url)