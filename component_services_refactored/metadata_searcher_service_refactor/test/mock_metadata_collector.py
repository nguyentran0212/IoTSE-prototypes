#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 17:01:17 2018

@author: nguyentran
"""

from flask import Flask
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

class Sensors(Resource):
    def get(self):
        response = None
        with open("mock_outputs/mock_output_metadata_collector.json") as f:
            response = json.load(f)
        return response
    
api.add_resource(Sensors, "/api/res-contents/879f06d0-ae81-4283-afc1-448c3dfff5ee")

if __name__ == "__main__":
    app.run(debug=True, port = 5001)