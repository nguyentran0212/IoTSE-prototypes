    # -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import unittest
import json
import requests

class TestServiceMethods(unittest.TestCase):
#    def setUp(self):
#        # Load the Web service for testing
#        self.service_app = main.app
#        self.service_app.run()
    
    def assert_post_request(self, input_file, output_correct_file, url, comparator, callback = False):
        # Load the input to send
        input_POST = None
        with open(input_file) as f:
            input_POST = json.load(f)
        
        # Load the output data to compare
        output_correct = None
        with open(output_correct_file) as f:
            output_correct = json.load(f)

        # Get the output from the service    
        r = requests.post(url, json = input_POST, headers = {"content-type":"application/json"})
        # If callback is not required, return the JSON of response and finish.
        if not callback:
            return r.json()
        redirect_URL = r.json()["payload"]["url"]
        r = requests.get(redirect_URL)
        output_from_service = r.json()
        
        # Remove metadata that are randomized by session ID
        try:
            del output_correct["workflow_id"]
            del output_correct["sender"]
            
            del output_from_service["workflow_id"]
            del output_from_service["sender"]
        except KeyError:
            pass
        
        return comparator(output_from_service, output_correct)

    def test_aggregator_direct(self):
        def comparator(*args):
#            print(args[0])
            return True

        # Submit the metadata search results
        self.assert_post_request("sample_inputs_outputs/input_metadata_direct.json", "sample_inputs_outputs/input_metadata_direct.json", "http://localhost:5000/api/agg_results", comparator)        
        
        # Submit the reading search results and assert the result
        assertResult = self.assert_post_request("sample_inputs_outputs/input_reading_direct.json", "sample_inputs_outputs/input_reading_direct.json", "http://localhost:5000/api/agg_results", comparator, callback=True)        
        self.assertTrue(assertResult)
    
#    def test_aggregator_indirect(self):
#        def comparator(*args):
##            print(args[0])
#            return True
#
#        # Submit the metadata search results
#        self.assert_post_request("sample_inputs_outputs/input_metadata_indirect.json", "sample_inputs_outputs/input_metadata_indirect.json", "http://localhost:5000/api/agg_results", comparator)        
#        
#        # Submit the reading search results and assert the result
#        assertResult = self.assert_post_request("sample_inputs_outputs/input_reading_indirect.json", "sample_inputs_outputs/input_reading_indirect.json", "http://localhost:5000/api/agg_results", comparator, callback=True)        
#        self.assertTrue(assertResult)
        
if __name__ == "__main__":
    unittest.main()