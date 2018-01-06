#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 13:15:52 2018

@author: nguyentran
"""
from lib.abstract_services import AbsStorageService

class StorageService(AbsStorageService):
    def _insert(self, res_contents_url, wf_id = ""):
        """
        Retrieve set of resources at the targeted URL and insert them
        to the database
        """
#        with open("test_cookie.txt", "a") as f:
#            f.write("From %s: %s\n" % (self, wf_id))
        return "collected content to storage"
    
    def _getSingleResource(self, res_id, wf_id = ""):
        """
        Get a single resource from the storage
        """
#        with open("test_cookie.txt", "a") as f:
#            f.write("From %s: %s\n" % (self, wf_id))
        return {}