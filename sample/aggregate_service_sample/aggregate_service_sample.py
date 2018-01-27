#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 14:21:58 2018

@author: nguyentran
"""

from lib.abstract_services import AbsAggregatorService

class AggregateService(AbsAggregatorService):
    processing_urls = {}
    
    def _store(self, result_url, wf_id = ""):
        self.addResultURL(result_url, wf_id)
        return "aggregator/api/results/%s" % wf_id
        
    def _aggregate(self, query_id, wf_id = ""):
        """
        This function returns the set of results generated from a previous query
        """
#        with open("test_cookie.txt", "a") as f:
#            f.write("From %s: %s\n" % (self, wf_id))
        return self.processing_urls[query_id]
    
    def addResultURL(self, result_url, wf_id):
        currentUrls = self.processing_urls.get(wf_id, None)
        if currentUrls is None:
            self.processing_urls[wf_id] = [result_url]
        else:
            self.processing_urls[wf_id].append(result_url)