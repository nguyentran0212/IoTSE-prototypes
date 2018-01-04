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
    def __init__(self, msg_type, sender, msg):
        self.type = msg_type
        self.sender = sender
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
    def __init__(self, sender, msg, res_ids):
        super().__init__(self.msg_type, sender, msg)
        self._add_payload("res_ids", res_ids)

        
class CollectorPostResMessage(Message):
    """
    Collector uses this message to return the timestamp and id of the collected
    batch of IoT content
    """
    msg_type = "CollectorPostResMessage"
    def __init__(self, sender, msg, res_contents_url):
        super().__init__(self.msg_type, sender, msg)
        self._add_payload("res_contents_url", res_contents_url)
        
class CollectorGetResMessage(Message):
    """
    Collector uses this message to return the batch of IoT content corresponding
    to the given timestamp
    Storage service uses this message to collect the batch of IoT content corresponding to 
    the given timestamp
    """
    msg_type = "CollectorGetResMessage"
    def __init__(self, sender, msg, iot_contents):
        super().__init__(self.msg_type, sender, msg)
        self._add_payload("iot_contents", iot_contents)
    
class StoragePostResMessage(Message):
    """
    Storage use this message to let client knows that it finished adding new iot content
    to the database
    """
    msg_type = "StoragePostResMessage"
    def __init__(self, sender):
        super().__init__(self.msg_type, sender, "Finish inserting IoT content to storage")
    
class SearcherPostQueryMessage(Message):
    """
    Search service uses this message to return the url of generated list of search results
    """
    msg_type = "SearcherPostQueryMessage"
    def __init__(self, sender, msg, result_url):
        super().__init__(self.msg_type, sender, msg)
        self._add_payload("result_url", result_url)
    
class SearcherGetResultMessage(Message):
    """
    Search service uses this message to return the list of resources in the search result
    to client
    """
    msg_type = "SearcherGetResultMessage"
    def __init__(self, sender, msg, results):
        super().__init__(self.msg_type, sender, msg)
        self._add_payload("results", results)
    
if __name__ == "__main__":
    msg = DetectorGetResMessage("Detector Service 1", "This is a message!", ["Res1", "Res1", "Res1", "Res1"])
    print(msg.to_json())      