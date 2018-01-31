#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 14:21:58 2018

@author: nguyentran
"""

import redis
import pickle
import lib.entity as entity
from lib.abstract_services import AbsAggregatorService
from pprint import pprint

class AggregateService(AbsAggregatorService):
    def __init__(self, redis_host = "localhost", redis_port = 6379, redis_db = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_client = redis.StrictRedis(host = redis_host, port = redis_port, db = redis_db)
        self.redis_query_id_key = "aggregator:query_id:"
        self.redis_agg_result_key = "aggregator:results:query_id:"
        
    
    def _store(self, result_set, wf_id = ""):
#        self.addResultURL(result_url, wf_id)
#        print(result_set.to_dict())
        query_ID = result_set.query_ID
        self.addResultSet(query_ID, result_set)
        return result_set.query_ID
        
    def _aggregate(self, query_ID, wf_id = ""):
        """
        This function returns the set of results generated from a previous query
        """
        """
        If the aggregation has been done previously, return the existing results.
        """
        p_aggregated_results = self.redis_client.get(self.redis_agg_result_key + query_ID)
        if p_aggregated_results is not None:
            print("Load the previously aggregated results")
            return pickle.loads(p_aggregated_results)
        
        """
        Otherwise, do the processing ... save the aggregated results, and return
        """
        p_current_sets = self.redis_client.get(self.redis_query_id_key + query_ID)
        current_sets = None
        try:
            current_sets = pickle.loads(p_current_sets)
        except TypeError:
            return None
        result_set = self.process(current_sets)
        
        """
        ... save the aggregated results, and return
        """
        p_result_set = pickle.dumps(result_set)
        self.redis_client.set(self.redis_agg_result_key + query_ID, p_result_set)
        print("Generate aggregated results, save to the database, and return")
        return result_set

    def process(self, result_sets):
        if not result_sets:
            return None
        else:
            agg_results_dict = {}
            """
            Use the first set of results as the seed for comparison
            """
            for result in result_sets[0].results:
                agg_results_dict[result[0]["ID"]] = [(result[0], result[1])]
    
            """
            Compare each item in the remaining set with the seed. If the ID is matching,
            then append IoT content info and score to the existing record
            """
            for result_set in result_sets[1:]:
                for result in result_set.results:
                    if agg_results_dict.get(result[0]["ID"], None) is None:
                        continue
                    else:
                        agg_results_dict[result[0]["ID"]].append((result[0], result[1]))
            
            """
            Keep only the list with highest length
            """
            agg_result_set = entity.ResultSet(query_ID = result_sets[0].query_ID, query_instance = result_sets[0].query_instance)
            for item in agg_results_dict.items():
                if len(item[1]) == len(result_sets):
                    """
                    This is an intersection of all result sets
                    """
                    agg_iot_content = entity.IoTContent(ID=item[0], metadata = {"type" : "aggregated_iot_content"}, content = {"aggregated_content" : [pair[0] for pair in item[1]]})
                    agg_score = {"aggregated_score" : [pair[1] for pair in item[1]]}
                    agg_result_set.add_IoTContent_score(IoTContent=agg_iot_content, score=agg_score)
            
            # Write to file to find out why this service not always return results
            with open("test_aggregator.txt", "a") as f:
                f.write("===========================\n")
                f.write("in process()\n")
                f.write("result_sets" + str(result_sets))
                f.write("agg_result_set" + str(agg_result_set))
            return agg_result_set
        
        
    
    def addResultSet(self, query_ID, result_set):
        p_current_sets = self.redis_client.get(self.redis_query_id_key + query_ID)
        if p_current_sets is None:
#            self.result_sets[query_ID] = [result_set]
            p_current_sets = pickle.dumps([result_set])
            self.redis_client.set(self.redis_query_id_key + query_ID, p_current_sets)
        else:
#            self.result_sets[query_ID].append(result_set)
            current_sets = pickle.loads(p_current_sets)
            current_sets.append(result_set)
            p_current_sets = pickle.dumps(current_sets)
            self.redis_client.set(self.redis_query_id_key + query_ID, p_current_sets)