#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 18:33:09 2018

@author: nguyentran
"""

from ..cs_kernel.base_builder import ComponentServiceBuilder as BaseBuilder
from . import resources
from . import conductor_client

class CollectorBuilder(BaseBuilder):
    def __init__(self):
        mapping = {"collector" : 
            ([(resources.ResContentsPost, "/api/res-contents"), (resources.ResContentsGet, "/api/res-contents/<req_id>")],
    [(conductor_client.CollectorConductorClient, "/api/res-contents")])}
        super().__init__(mapping)