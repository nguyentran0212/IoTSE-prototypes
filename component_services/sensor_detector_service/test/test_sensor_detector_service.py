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
    
    def assert_post_request(self, input_file, output_correct_file, url):
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
        
        return output_from_service == output_correct
    
    def test_detect_sensors_direct(self):
        assertResult = self.assert_post_request("sample_inputs_outputs/input_sensor_detector_direct.json", "sample_inputs_outputs/output_sensor_detector_direct.json", "http://localhost:5000/api/new-cont-ids")        
        self.assertTrue(assertResult)
        
    def test_detect_sensors_redirect(self):
        assertResult = self.assert_post_request("sample_inputs_outputs/input_sensor_detector_redirect.json", "sample_inputs_outputs/output_sensor_detector_direct.json", "http://localhost:5000/api/new-cont-ids")        
        self.assertTrue(assertResult)
        
if __name__ == "__main__":
    unittest.main()