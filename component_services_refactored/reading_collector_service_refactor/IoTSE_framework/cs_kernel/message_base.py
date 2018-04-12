#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 16:54:32 2018

@author: nguyentran
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