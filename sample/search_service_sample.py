#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 13:22:31 2018

@author: nguyentran
"""
from abstract_services import AbsSearchService

class SearchService(AbsSearchService):
    def _query(self, query):
        """
        This function search the database to resolve the given query
        and put search result into a storage space, and return the identifier
        of that list of search results to the client
        """
        return "127.0.0.1:5000/results/<time-stamp-id>"
        
    def _getResult(self, result_id):
        """
        This function returns the set of results generated from a previous query
        """
        return []