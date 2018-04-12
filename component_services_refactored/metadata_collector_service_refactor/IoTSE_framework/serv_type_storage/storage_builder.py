#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 18:33:09 2018

@author: nguyentran
"""

from ..cs_kernel.base_builder import ComponentServiceBuilder as BaseBuilder
from . import resources
from . import conductor_client

class StorageBuilder(BaseBuilder):
    def __init__(self):
        mapping = {"storage" : 
            ([(resources.Contents, "/api/iot-contents")],
    [(conductor_client.StorageConductorClient, "/api/iot-contents")])}
        super().__init__(mapping)