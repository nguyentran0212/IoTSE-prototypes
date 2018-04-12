#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 18:33:09 2018

@author: nguyentran
"""

from ..cs_kernel.base_builder import ComponentServiceBuilder as BaseBuilder
from . import resources
from . import conductor_client

class DetectorBuilder(BaseBuilder):
    def __init__(self):
        mapping = {"detector" : 
            ([(resources.NewResIDsPost, "/api/new-cont-ids"), (resources.NewResIDsGet, "/api/new-cont-ids/<req_id>")],
    [(conductor_client.DetectorConductorClient, "/api/new-cont-ids")])}
        super().__init__(mapping)