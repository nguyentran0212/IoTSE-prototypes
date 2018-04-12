#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 14:27:41 2018

@author: nguyentran
"""

from IoTSE_framework.serv_type_facade.facade_builder import FacadeBuilder as ComponentServiceBuilder

cs_builder = ComponentServiceBuilder()
#    cs = cs_builder.build("config.json", conn_to_conductor=True)
cs = cs_builder.build("config.json", conn_to_conductor=True)
cs.boot()
app = cs.app