#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 18:33:09 2018

@author: nguyentran
"""

from ..cs_kernel.base_builder import ComponentServiceBuilder as BaseBuilder
from . import resources
from . import conductor_client

class SearcherBuilder(BaseBuilder):
    def __init__(self):
        mapping = {"search" : 
            ([(resources.Queries, "/api/queries"), (resources.Result, "/api/results/<query_id>")],
    [(conductor_client.SearcherConductorClient, "/api/queries")])}
        super().__init__(mapping)