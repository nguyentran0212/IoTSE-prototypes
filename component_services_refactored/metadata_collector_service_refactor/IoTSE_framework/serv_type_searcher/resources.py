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
# /api/queries
#==================================
class Queries(AbsResource):
    """
    Served by a searcher service. It represents the set of all queries handled 
    by a searcher service
    """
    
    def post(self):
        """
        POST request to this resource sends a query and invoke the search process
        It returns URL of the newly created result resource corresponding to the incoming query
        """
        workflow_id = self.extract_workflow_id()           
        query = self.extract_from_payload("query")
        query = entity.Query(query_dict=query)
        query_id = self.service.query(query, wf_id = workflow_id)
        result_url = "%s/%s" % (self.generate_host_port_endpoint(endpoint = "/api/results/<query_id>"), query_id)
        msg = message.CallbackMessage(request.url, "Finished query. Find the result at the included URL", result_url, workflow_id = workflow_id)
        return msg.to_dict() , 201
    
#==================================
# /api/results
#==================================
class Result(AbsResource):
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
        result_set = self.service.getResult(query_id, wf_id = workflow_id)
        msg = message.ResultSetMessage(request.url, "Results", result_set, workflow_id = workflow_id)
        return msg.to_dict()