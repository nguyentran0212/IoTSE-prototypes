#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 13:22:31 2018

@author: nguyentran
"""
from lib.abstract_services import AbsSearcherService
import lib.entity as entity
import redis
import pickle
from pymongo import MongoClient
from pprint import pprint

class SampleData():
    def __init__(self):
        query1 = entity.Query("query_1", {"temperature" : "q234", "type" : "sensor data"})
        result_set = entity.ResultSet("query_1", query1.to_dict())
        iot_content1 = entity.IoTContent("resource_1", {"type" : "sensor data"}, {"temperature" : 234})
        iot_content2 = entity.IoTContent("resource_2", {"type" : "sensor data"}, {"temperature" : 234})
        iot_content3 = entity.IoTContent("resource_3", {"type" : "sensor data"}, {"temperature" : 234})
        result_set.add_IoTContent_score(iot_content1, {"score" : 50})
        result_set.add_IoTContent_score(iot_content2, {"score" : 10})
        result_set.add_IoTContent_score(iot_content3, {"score" : 70})
        self.result_set = result_set

#sample_data = SampleData()

class SearcherService(AbsSearcherService):
    def __init__(self, redis_host = "localhost", redis_port = 6379, redis_db = 0, mongo_host = "localhost", mongo_port = 27017, query_type = "metadata_query", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query_type = query_type
        # Create client to redis database
        self.redis_client = redis.StrictRedis(host = redis_host, port = redis_port, db = redis_db)
        self.redis_query_id_key = "searcher:query_id:"
        # Create client to mongo database
        self.mongo_client = MongoClient(host = mongo_host, port = mongo_port)
        self.mongo_db = self.mongo_client.sensor_metadata_db
        self.mongo_col = self.mongo_db.sensor_metadata_collection
    
    def _query(self, query, wf_id = ""):
        """
        This function search the database to resolve the given query
        and put search result into a storage space, and return the identifier
        of that list of search results to the client
        """
        # Extract the relevant query from the input query message
        query_id = query.query_ID
        query_content = query.query_content.get(self.query_type, {})
        pprint(query_content)
        
        # Perform the search to find sensors
        result_curs = self.mongo_col.find(query_content)
        result_set = entity.ResultSet(query_ID = query_id, query_instance = query)
        for result in result_curs:
            score = {"score" : 100}
            iot_content = entity.IoTContent(iot_content_dict=result)
            result_set.add_IoTContent_score(iot_content.to_dict(), score)

        # Store result set in Redis and return a key for client to retrieve results
        p_result_set = pickle.dumps(result_set)
        self.redis_client.set(self.redis_query_id_key + query_id, p_result_set)
        return query_id
        
    
    def _getResult(self, query_id, wf_id = ""):
        """
        This function returns the set of results generated from a previous query
        """
#        with open("test_cookie.txt", "a") as f:
#            f.write("From %s: %s\n" % (self, wf_id))
        p_result_set = self.redis_client.get(self.redis_query_id_key + query_id)
        result_set = pickle.loads(p_result_set)
        # Following lines are only for supporting the mockup data
        result_set.query_ID = query_id
        result_set.query_instance["query_ID"] = query_id
        return result_set