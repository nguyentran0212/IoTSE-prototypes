#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 18:27:34 2018

@author: nguyentran
"""

from ISEPLib.abstract_services import AbsCollectorService
import time
import math
import ISEPLib.entity as entity
import uuid
import redis
import requests
import pickle

class SampleData():
    def __init__(self, *args, **kwargs):
        iot_content1 = entity.IoTContent("source 1", {"type" : "temp sensor"}, {"value" : 34})
        iot_content2 = entity.IoTContent("source 2", {"type" : "humidity sensor"}, {"value" : 54})
        iot_content3 = entity.IoTContent("source 3", {"type" : "light sensor"}, {"value" : 5})
        self.req_id = "123456"    
        self.data = {self.req_id : [iot_content1, iot_content2, iot_content3]}
        
sample_data = SampleData()

class CollectorService(AbsCollectorService):
    def __init__(self, redis_host = "localhost", redis_port = 6379, redis_db = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_client = redis.StrictRedis(host = redis_host, port = redis_port, db = redis_db)
        self.redis_reading_collector_key = "reading_collector_service:key:"
    
    def _collect(self, sensor_urls, wf_id = ""):
        sensor_reading_objects = []
        for sensor_url in sensor_urls:
            sensor_reading_objects.append(self.collect_reading_from_sensor_url(sensor_url))
        
        req_id = self.generate_key()
        key = "%s%s" % (self.redis_reading_collector_key, req_id)
        p_sensor_reading_objects = pickle.dumps(sensor_reading_objects)
        self.redis_client.set(key, p_sensor_reading_objects)
        return req_id
    
    def _lookup(self, req_id, wf_id = ""):
        key = "%s%s" % (self.redis_reading_collector_key, req_id)
        p_sensor_reading_objects = self.redis_client.get(key)
        if p_sensor_reading_objects is None:
            return None
        else:
            sensor_reading_objects = pickle.loads(p_sensor_reading_objects)
            return sensor_reading_objects

    
    def collect_reading_from_sensor_url(self, sensor_url):
        """
        Assume that the given source is compliant to OGC SensorThing API
        """
        observation_url = "%s/%s" % (sensor_url, "Observations")
        r = requests.get(observation_url)
        sensor_observation = r.json()
        try:
            del sensor_observation["@iot.id"]
            del sensor_observation["@iot.selfLink"]
            del sensor_observation["Datastream@iot.navigationLink"]
            del sensor_observation["FeatureOfInterest@iot.navigationLink"]
        except KeyError:
            pass
        sensor_reading_object = entity.IoTContent(sensor_url, {"type" : "sensor_reading"}, sensor_observation)
        return sensor_reading_object
    
    def generate_key(self):
        return str(uuid.uuid4())