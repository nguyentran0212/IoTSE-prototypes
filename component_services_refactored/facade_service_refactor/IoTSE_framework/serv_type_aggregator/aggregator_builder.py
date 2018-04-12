#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 18:33:09 2018

@author: nguyentran
"""

from ..cs_kernel.base_builder import ComponentServiceBuilder as BaseBuilder
from . import resources
from . import conductor_client

class AggregatorBuilder(BaseBuilder):
    def __init__(self):
        mapping = {"aggregator" : 
            ([(resources.AggregatorResultsPost, "/api/agg_results"), (resources.AggregatorResultsGet, "/api/agg_results/<query_id>")],
    [(conductor_client.AggregatorConductorClient, "/api/agg_results")])}
        super().__init__(mapping)
