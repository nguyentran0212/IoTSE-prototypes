#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 14:27:41 2018

@author: nguyentran
"""
from IoTSE_framework.serv_type_storage.storage_builder import StorageBuilder as StorageBuilder
from IoTSE_framework.serv_type_searcher.searcher_builder import SearcherBuilder as SearcherBuilder


storage_builder = StorageBuilder()
searcher_builder = SearcherBuilder()
cs_builder = storage_builder.combine(searcher_builder)

cs = cs_builder.build("config.json", conn_to_conductor=True)
cs.boot()
app = cs.app
