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
# /queries
#==================================
class FacadeQueries(AbsResource):
    """
    Served by a facade service. It provides the entry point to the system for 
    search clients
    """
    def post(self):
        """
        POST request to this resource sends a query and invoke the search process
        It returns URL of the newly created result resource corresponding to the incoming query
        """
        query_content = request.get_json(force=True)
        query_id, workflow_id = self.service.query(query_content)
        result_url = "%s/%s" % (self.generate_host_port_endpoint(endpoint = "/results/<query_id>"), query_id)
        msg = message.CallbackMessage(request.url, "Finished query. Find the result at the included URL", result_url, workflow_id = workflow_id)

        return msg.to_dict() , 201
    
#==================================
# /results/<result_id>
#==================================
class FacadeResultGet(AbsResource):
    """
    Served by a facade service. It provides and endpoint for search clients
    to retrieve the status of their submitted queries
    """
    def get(self, query_id):
        """
        GET request to this resource check the current state of the given query
        and return the url of the server holding result list if it is available
        """
        workflow_id = self.extract_workflow_id()          
        result_set = self.service.getResult(query_id, wf_id = workflow_id)
        msg = None
        if type(result_set) is not entity.ResultSet:
            result_url = "%s/%s" % (self.generate_host_port_endpoint(), query_id)
            msg = message.CallbackMessage(request.url, "Result is not available. Please check again later.", result_url, workflow_id = workflow_id)
        else:
            msg = message.ResultSetMessage(request.url, "Results", result_set, workflow_id = workflow_id)
        return msg.to_dict()
    
#==================================
# /results
#==================================
class FacadeResultPost(AbsResource):
    """
    Served by a facade service. This endpoint accepts updates from other services
    to update the state of a query under processing
    """
    def post(self):
        """
        POST request to this resource to update the URL pointing to the result list
        of a processing query
        """
        workflow_id = self.extract_workflow_id()
        result_set = self.get_result_set(workflow_id=workflow_id)
        query_id = result_set.query_ID
        self.service.updateResult(query_id, result_set)
        result_url = "%s/%s" % (self.generate_host_port_endpoint(), query_id)
        msg = message.CallbackMessage(request.url, "Updated results of query %s" % query_id, result_url, workflow_id = workflow_id)
        return msg.to_dict(), 201