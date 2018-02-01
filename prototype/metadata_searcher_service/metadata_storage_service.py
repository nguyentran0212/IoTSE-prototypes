#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 13:15:52 2018

@author: nguyentran
"""
from ISEPLib.abstract_services import AbsStorageService
from pymongo import MongoClient
from pprint import pprint

class StorageService(AbsStorageService):
    def __init__(self, mongo_host = "localhost", mongo_port = 27017, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongo_client = MongoClient(host = mongo_host, port = int(mongo_port))
        self.mongo_db = self.mongo_client.sensor_metadata_db
        self.mongo_col = self.mongo_db.sensor_metadata_collection
    
    def _insert(self, iot_contents, wf_id = ""):
        """
        Retrieve set of resources at the targeted URL and insert them
        to the database
        """
        self.mongo_col.create_index("ID", unique = True)
        
        for iot_content in iot_contents: 
            temp_dict = {"ID" : iot_content.ID, "metadata" : {"type" : "sensor_metadata"}, "content" : iot_content.content}
            self.mongo_col.update_one({"ID" : iot_content.ID}, {"$set" : temp_dict}, upsert = True)

        return "stored collected sensor metadata"
    
    def _getSingleResource(self, res_id, wf_id = ""):
        """
        Get a single resource from the storage
        """
#        with open("test_cookie.txt", "a") as f:
#            f.write("From %s: %s\n" % (self, wf_id))
        return {}