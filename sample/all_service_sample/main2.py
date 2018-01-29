#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 15:34:25 2018

@author: nguyentran
"""

import lib.message as message
import lib.entity as entity
import json

iot_content1 = entity.IoTContent("resource 1", {"type" : "sensor data"}, {"temperature" : 234})
iot_content2 = entity.IoTContent("resource 2", {"type" : "sensor data"}, {"temperature" : 234})
iot_content3 = entity.IoTContent("resource 3", {"type" : "sensor data"}, {"temperature" : 234})
iot_content4 = entity.IoTContent(iot_content_dict={"ID" : "resource 4", "metadata" : {"type" : "sensor data"}, "content" : {"temperature" : 234}})
iot_contents = [iot_content1, iot_content2, iot_content3, iot_content4]

#print(iot_contents)
#
#iot_contents_message = message.IoTContentsMessage("sender", "msg", iot_contents)
#print(iot_contents_message.to_json())

query1 = entity.Query("query 1", {"temperature" : "q234", "type" : "sensor data"})
query2 = entity.Query(query_dict={"query_ID" : "query 2", "query_content" : {"temperature" : "q234", "type" : "sensor data"}})

result_set = entity.ResultSet("query 1", query1.to_dict())
result_set.add_IoTContent_score(iot_content1, {"score" : 50})
result_set.add_IoTContent_score(iot_content2, {"score" : 10})
result_set.add_IoTContent_score(iot_content3, {"score" : 70})
#print(result_set.to_dict())

query_message = message.QueryMessage("sender", "msg", query1)
print(query_message.to_json())

result_set_message = message.ResultSetMessage("sender", "msg", result_set)
#print(result_set_message.to_dict())
#print(result_set_message.to_json())

callback_message = message.CallbackMessage("sender", "msg", "123.543.546.235:5050/api/items/25")
#print(callback_message.to_json())
