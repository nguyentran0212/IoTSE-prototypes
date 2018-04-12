#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 16:59:44 2018

@author: nguyentran
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 12:33:00 2018

@author: nguyentran
"""

from ..abs_IoTSE_resource.abs_IoTSE_resource import AbsIoTSEResource as AbsResource
from ..IoTSE_models_messages import IoTSE_messages as message
from ..IoTSE_models_messages import IoTSE_entities as entity

from flask import abort, request

#==================================
# /api/agg_results
#==================================
class AggregatorResultsPost(AbsResource):
    """
    Served by an aggregator service. It represents the set of all lists of search results
    submitted to the aggregator for aggregation
    """
    def post(self):
        """
        POST request to this resource sends a result URL and invoke the store process
        It returns URL to /api/results/<query_id> to retrieve aggregated results
        
        Expect a message in the format of SearcherPostQueryMessage
        """
        workflow_id = self.extract_workflow_id()
        result_set = self.get_result_set(workflow_id=workflow_id)
        query_id = self.service.store(result_set, wf_id = workflow_id)
        aggregated_result_url = "%s/%s" % (self.generate_host_port_endpoint(), query_id)
        msg = message.CallbackMessage(request.url, "Added result URL for the query %s. Find the result at the included URL" % (workflow_id), aggregated_result_url, workflow_id = workflow_id)
        return msg.to_dict() , 201
    
#==================================
# /api/agg_results/<query_id>
#==================================
class AggregatorResultsGet(AbsResource):
    """
    Served by a searcher service. It represents the set of all results generated
    by a searcher service
    """
    def get(self, query_id):
        """
        GET request to this resource returns an individual resource item in
        the storage
        """
        workflow_id = self.extract_workflow_id()
        result_set = self.service.aggregate(query_id, wf_id = workflow_id)
        if type(result_set) is not entity.ResultSet:
            abort(404)
        msg = message.ResultSetMessage(request.url, "Aggregated Search Results", result_set, workflow_id = workflow_id)
        return msg.to_dict()