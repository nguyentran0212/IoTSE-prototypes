#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 14:27:41 2018

@author: nguyentran
"""

from IoTSE_framework.serv_type_aggregator.aggregator_builder import AggregatorBuilder as ComponentServiceBuilder

cs_builder = ComponentServiceBuilder()
cs = cs_builder.build("config.json", conn_to_conductor=False)
cs.boot()
app = cs.app
app.run()