#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 18:33:09 2018

@author: nguyentran
"""

from ..cs_kernel.base_builder import ComponentServiceBuilder as BaseBuilder
from . import resources
from . import conductor_client

class FacadeBuilder(BaseBuilder):
    def __init__(self):
        mapping = {"facade" : 
            ([(resources.FacadeQueries, "/queries"), (resources.FacadeResultPost, "/results"), (resources.FacadeResultGet, "/results/<query_id>")],
    [(conductor_client.FacadeConductorClient, "/results")])}
        super().__init__(mapping)
