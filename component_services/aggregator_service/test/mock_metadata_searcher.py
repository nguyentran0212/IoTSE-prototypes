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

class Results(Resource):
    def get(self):
        response = None
        with open("mock_outputs/mock_output_searcher_metadata.json") as f:
            response = json.load(f)
        return response
    
api.add_resource(Results, "/api/results/query_1")

if __name__ == "__main__":
    app.run(debug=True, port = 5001)