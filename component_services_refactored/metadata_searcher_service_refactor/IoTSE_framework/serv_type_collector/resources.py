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

from flask import abort, request

#==================================
# /api/res-contents
#==================================
class ResContentsPost(AbsResource):
    """
    This resource is served by collector services
    """
    def post(self):
        """
        Endpoint: /api/res-contents
        
        POST request to this resource invoke the collection process for IoT content
        at the given identifiers. Content is timestamped and store.
        Every new POST request replaces the previous timestamp with a newer one
        """
        workflow_id = self.extract_workflow_id()

        # Get IoT content either directly from the message, or via call back        
        iot_contents = self.get_iot_contents(workflow_id=workflow_id)
        
        req_id = self.service.collect(iot_contents, request.host, wf_id = workflow_id)
        req_id = "%s/%s" % (self.generate_host_port_endpoint(), req_id)
        
        msg = message.CallbackMessage(request.url, "Invoked collection process. Poll the returned URL for results.", req_id, workflow_id = workflow_id)
        return msg.to_dict() , 201

#==================================
# /api/res-contents/<req_id>
#==================================
class ResContentsGet(AbsResource):
    """
    This resource is served by collector services
    """
    def get(self, req_id):
        workflow_id = self.extract_workflow_id()
#        with open("test_cookie.txt", "a") as f:
#            f.write("From ResContent: %s\n" % workflow_id)
            
        contents = self.service.lookup(req_id, wf_id = workflow_id)
        msg = message.IoTContentsMessage(request.url, "List of IoT content at the given req_id", contents, workflow_id = workflow_id)
        return msg.to_dict()