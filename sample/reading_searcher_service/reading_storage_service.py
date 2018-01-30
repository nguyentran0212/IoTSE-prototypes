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
        self.mongo_client = MongoClient(host = mongo_host, port = mongo_port)
        self.mongo_db = self.mongo_client.sensor_metadata_db
        self.mongo_col = self.mongo_db.sensor_readings_collection
    
    def _insert(self, iot_contents, wf_id = ""):
        """
        Retrieve set of resources at the targeted URL and insert them
        to the database
        """
        for iot_content in iot_contents: 
            temp_dict = {"ID" : iot_content.ID, "metadata" : {"type" : "sensor_reading"}, "content" : iot_content.content}
#            pprint(temp_dict)
            self.mongo_col.insert_one(temp_dict)
#        with open("test_cookie.txt", "a") as f:
#            f.write("From %s: %s\n" % (self, wf_id))
#        print([i.to_dict() for i in iot_contents])
        return "stored collected sensor metadata"
    
    def _getSingleResource(self, res_id, wf_id = ""):
        """
        Get a single resource from the storage
        """
#        with open("test_cookie.txt", "a") as f:
#            f.write("From %s: %s\n" % (self, wf_id))
        return {}