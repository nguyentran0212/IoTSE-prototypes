#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 13:15:52 2018

@author: nguyentran
"""
from lib.abstract_services import AbsStorageService
from pymongo import MongoClient
from pprint import pprint

class StorageService(AbsStorageService):
    def __init__(self, mongo_host = "localhost", mongo_port = 27017, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongo_client = MongoClient(host = mongo_host, port = int(mongo_port))
        self.mongo_db = self.mongo_client.sensor_readings_db
        self.mongo_col = self.mongo_db.sensor_readings_collection
    
    def _insert(self, iot_contents, wf_id = ""):
        """
        Insert a set of IoT content entities into database.
        Manually parse observation value from string to float before inserting.
        Skip over results that cannot be parse
        """
        self.mongo_col.create_index("ID", unique = True)
        
#        iot_contents_dict = []
        for iot_content in iot_contents: 
            try:
                iot_content.content["result"] = float(iot_content.content["result"])
            except KeyError:
                continue
            temp_dict = {"ID" : iot_content.ID, "metadata" : {"type" : "sensor_reading"}, "content" : iot_content.content}
            self.mongo_col.update_one({"ID" : iot_content.ID}, {"$set" : temp_dict}, upsert = True)

        return "stored collected sensor metadata"
    
    def _getSingleResource(self, res_id, wf_id = ""):
        """
        Get a single resource from the storage
        """
#        with open("test_cookie.txt", "a") as f:
#            f.write("From %s: %s\n" % (self, wf_id))
        return {}