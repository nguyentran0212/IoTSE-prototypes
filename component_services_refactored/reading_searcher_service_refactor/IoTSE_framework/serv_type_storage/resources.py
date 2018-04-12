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
# /api/iot-contents
#==================================
class Contents(AbsResource):
    """
    This resource is served by IoT resource storage
    """
    def post(self):
        
        workflow_id = self.extract_workflow_id()
            
        # Get IoT content either directly from the message, or via call back        
        iot_contents = self.get_iot_contents(workflow_id=workflow_id)
        
#        # Get the url of data to retrieve
#        res_contents_url = self.extract_from_payload("res_contents_url")
        
        # Get content from URl and add to the database
        self.service.insert(iot_contents, wf_id = workflow_id)
        
        url = self.generate_host_port_endpoint()
        msg = message.CallbackMessage(request.url, "Stored IoT content. Poll the returned URL for getting all stored IoT content.", url, workflow_id = workflow_id)
        
        return msg.to_dict(), 201 
    
#class Res(AbsResource):
#    """
#    This resource is served by IoT resource storage. It represents individual 
#    resource item
#    """
#    def get(self, res_id):
#        """
#        GET request to this resource returns an individual resource item in
#        the storage
#        """
#        workflow_id = self.extract_workflow_id()
##        with open("test_cookie.txt", "a") as f:
##            f.write("From Res: %s\n" % workflow_id)
#            
#        return {"res" : self.service.getSingleResource(res_id, wf_id = workflow_id)}