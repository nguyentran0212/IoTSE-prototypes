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
    
    def test_POST_output(self):
        # Load the output data to compare
        output_POST_correct = None
        with open("output_source_detector_POST.json") as f:
            output_POST_correct = json.load(f)
        
        r = requests.post("http://localhost:5000/api/new-cont-ids")
        output_POST_from_service = r.json()
        
        self.assertEqual(output_POST_from_service, output_POST_correct)
        
    def test_GET_output(self):
        # Load the output data to compare
        output_GET_correct = None
        with open("output_source_detector_GET.json") as f:
            output_GET_correct = json.load(f)
        
        r = requests.get("http://localhost:5000/api/new-cont-ids/wsp")
        output_GET_from_service = r.json()
        
        self.assertEqual(output_GET_from_service, output_GET_correct)
        
if __name__ == "__main__":
    unittest.main()