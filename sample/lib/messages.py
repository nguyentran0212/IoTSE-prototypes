#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 16:08:08 2018

@author: nguyentran

This module contain classes representing messages exchanged between IoTSE
component services
"""

from abc import ABC, abstractmethod
import json

class Message(ABC):
    def __init__(self, msg_type, sender, msg, workflow_id):
        self.type = msg_type
        self.sender = sender
        self.workflow_id = workflow_id
        self.msg = msg
        self.payload = {}
        self.misc = None
        
    def _add_payload(self, key, value):
        self.payload[key] = value
        
    def to_json(self):
        return json.dumps(self.__dict__)
    
    def to_dict(self):
        return self.__dict__
  
class DetectorGetResMessage(Message):
    """
    Detector uses this message to return a list of resource ids to clients
    Collector uses this message as the input to its POST request on res-contents resource
    """
    msg_type = "DetectorGetResMessage"
    def __init__(self, sender, msg, res_ids, workflow_id = ""):
        super().__init__(self.msg_type, sender, msg, workflow_id = workflow_id)
        self._add_payload("res_ids", res_ids)

        
class CollectorPostResMessage(Message):
    """
    Collector uses this message to return the timestamp and id of the collected
    batch of IoT content
    """
    msg_type = "CollectorPostResMessage"
    def __init__(self, sender, msg, res_contents_url, workflow_id = ""):
        super().__init__(self.msg_type, sender, msg, workflow_id = workflow_id)
        self._add_payload("res_contents_url", res_contents_url)
        
class CollectorGetResMessage(Message):
    """
    Collector uses this message to return the batch of IoT content corresponding
    to the given timestamp
    Storage service uses this message to collect the batch of IoT content corresponding to 
    the given timestamp
    """
    msg_type = "CollectorGetResMessage"
    def __init__(self, sender, msg, iot_contents, workflow_id = ""):
        super().__init__(self.msg_type, sender, msg, workflow_id = workflow_id)
        self._add_payload("iot_contents", iot_contents)
    
class StoragePostResMessage(Message):
    """
    Storage use this message to let client knows that it finished adding new iot content
    to the database
    """
    msg_type = "StoragePostResMessage"
    def __init__(self, sender, workflow_id = ""):
        super().__init__(self.msg_type, sender, "Finish inserting IoT content to storage", workflow_id = workflow_id)
    
class SearcherPostQueryMessage(Message):
    """
    Search service uses this message to return the url of generated list of search results
    """
    msg_type = "SearcherPostQueryMessage"
    def __init__(self, sender, msg, result_url, workflow_id = ""):
        super().__init__(self.msg_type, sender, msg, workflow_id = workflow_id)
        self._add_payload("result_url", result_url)
    
class SearcherGetResultMessage(Message):
    """
    Search service uses this message to return the list of resources in the search result
    to client
    """
    msg_type = "SearcherGetResultMessage"
    def __init__(self, sender, msg, results, workflow_id = ""):
        super().__init__(self.msg_type, sender, msg, workflow_id = workflow_id)
        self._add_payload("results", results)
    
class FacadePostQueryMessage(Message):
    """
    Facade service uses this message to return the id of the result for 
    client to poll and check
    """
    msg_type = "FacadePostQueryMessage"
    def __init__(self, sender, msg, result_url_to_poll, workflow_id = ""):
        super().__init__(self.msg_type, sender, msg, workflow_id = workflow_id)
        self._add_payload("result_url", result_url_to_poll)
        
class FacadeGetResultMessage(Message):
    """
    Facade service uses this message to return the url of the result list
    for client to retrieve
    """
    msg_type = "FacadeGetResultMessage"
    def __init__(self, sender, msg, result_url_to_poll, workflow_id = ""):
        super().__init__(self.msg_type, sender, msg, workflow_id = workflow_id)
        self._add_payload("result_url", result_url_to_poll)
        
class FacadePostResultMessage(Message):
    """
    Facade service uses this message to notify the sender of the update
    that it received and stored the sent URL of search results list
    """
    msg_type = "FacadePostResultMessage"
    def __init__(self, sender, msg, workflow_id = ""):
        super().__init__(self.msg_type, sender, msg, workflow_id = workflow_id)
    
if __name__ == "__main__":
    msg = DetectorGetResMessage("Detector Service 1", "This is a message!", ["Res1", "Res1", "Res1", "Res1"])
    print(msg.to_json())      