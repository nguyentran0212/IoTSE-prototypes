#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 16:51:41 2018

@author: nguyentran

Base Entity class allows defining concrete types of entities
"""
from abc import ABC, abstractmethod

class Entity(ABC):
    def __init__(self):
        pass
    
    def to_dict(self):
        return self.__dict__
    
    def from_dict(self):
        """
        Specify the logic to create an entity object from a dictionary
        """
        pass