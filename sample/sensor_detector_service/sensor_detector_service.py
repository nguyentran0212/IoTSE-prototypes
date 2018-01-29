#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 18:06:56 2018

@author: nguyentran
"""

from lib.abstract_services import AbsDetectorService
import lib.entity as entity
import uuid
import redis
import requests
import pickle

class DetectorService(AbsDetectorService):
    def __init__(self, wsr_host_port = None, redis_host = "localhost", redis_port = 6379, redis_db = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        iot_source = entity.IoTContent("wsr_1", {"type" : "sensor source"}, {"url" : wsr_host_port})
        self.sources = {"wsr" : [iot_source]}
        self.redis_client = redis.StrictRedis(host = redis_host, port = redis_port, db = redis_db)
        self.redis_query_id_key = "sensor_detector_service:key:"
    
    def _detect(self, iot_contents = [], wf_id = ""):
        """
        Accept a list of iot content storing source URLs, request URLs to
        get list of sensors, turn list of sensors into list of IoT content, 
        store, and return a key for future retrieval
        """
        source_urls = [iot_content["content"]["url"] for iot_content in iot_contents]
        sensor_urls = []
        for source_url in source_urls:
            sensor_urls.extend(self.detect_sensors_from_source(source_url))
            
        req_id = self.generate_key()
        key = "%s%s" % (self.redis_query_id_key, req_id)
        p_sensor_urls = pickle.dumps(sensor_urls)
        self.redis_client.set(key, p_sensor_urls)
        return req_id
    
    def get_detect_result(self, req_id = "", wf_id = ""):
        """
        retrieve the list of IoT content sources
        """
        key = "%s%s" % (self.redis_query_id_key, req_id)
        p_sensor_urls = self.redis_client.get(key)
        if p_sensor_urls is None:
            return None
        else:
            sensor_urls = pickle.loads(p_sensor_urls)
            sensor_url_objects = []
            for sensor_url in sensor_urls:
                sensor_url_object = entity.IoTContent(sensor_url, {"type" : "sensor url"}, {"url" : sensor_url})
                sensor_url_objects.append(sensor_url_object)
            return sensor_url_objects
    
    def detect_sensors_from_source(self, source_url):
        """
        Assume that the given source is compliant to OGC SensorThing API
        """
        sensors_url = "%s/%s" % (source_url, "Datastreams")
        r = requests.get(sensors_url)
        datastreams_list = r.json()["value"]
        sensor_urls = []
        for datastream in datastreams_list:
            datastream_id = datastream["@iot.id"]
            sensor_url = "%s/%s(%s)" % (source_url, "Datastreams", datastream_id)
            sensor_urls.append(sensor_url)
        return sensor_urls
    
    def generate_key(self):
        return str(uuid.uuid4())