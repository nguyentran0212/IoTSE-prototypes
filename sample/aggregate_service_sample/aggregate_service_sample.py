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

class AggregateService(AbsAggregatorService):
    def __init__(self, redis_host = "localhost", redis_port = 6379, redis_db = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_client = redis.StrictRedis(host = redis_host, port = redis_port, db = redis_db)
        self.redis_query_id_key = "aggregator:query_id:"
    
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
        p_current_sets = self.redis_client.get(self.redis_query_id_key + query_ID)
        current_sets = None
        try:
            current_sets = pickle.loads(p_current_sets)
        except TypeError:
            return None
        result_set = self.process(current_sets)
        return result_set

    def process(self, result_sets):
        if not result_sets:
            return None
        else:
            return result_sets[0]
    
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