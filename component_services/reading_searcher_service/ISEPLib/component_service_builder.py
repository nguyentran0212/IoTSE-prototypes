#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 10:56:36 2018

@author: nguyentran
"""
import json
import os
from ISEPLib.component_service import ComponentService
from importlib import import_module

class ComponentServiceBuilder:
    def load_services(self, config_json_path, wf_host_port, env_vars):
        """
        args and kwargs in json config are specified in design time
        additional_kwargs contains kwargs provided in run time
        """
        def load_module_configs(config_json_path):
            module_configs = []
            with open(config_json_path, "r") as file:
                module_configs = json.load(file)["services"]
            
            return module_configs
        
        def load_service_classes(module_configs, env_vars):
            classes = []
            for module_config in module_configs:
                module_config = module_config["service"]
                module = import_module(module_config["module"], package=module_config["package"])
                kwargs = module_config["kwargs"]
                kwargs_env_vars = kwargs.copy()
                kwargs_env_vars.update(env_vars)
                class_args_kwargs = (module.__dict__[module_config["class"]], module_config["args"], kwargs_env_vars)
                classes.append(class_args_kwargs)
            return classes
        
        def instantiate_services(service_classes):
            services = []
            for cls, args, kwargs in service_classes:
                """
                Special case for facade service: inject wf_server_addr_port
                """
                if cls.serv_type == "facade":
                    # append wf_server_addr_port to kwargs of the service
                    kwargs["wf_server_path"] = "http://%s/api" % wf_host_port
                print("Instantiating service %s" % cls.serv_type)
                services.append(cls(*args, **kwargs))
            return services
        
        module_configs = load_module_configs(config_json_path)
        service_classes = load_service_classes(module_configs, env_vars)
        services = instantiate_services(service_classes)
        return services
    
    def load_env_vars(self, config_json_path):
        """
        load_env_vars loads declared environment variables from os.getenv. If they are not available,
        if uses the default value. Return a dictionary {param_name : param_value}
        """
        def load_var_declarations(config_json_path):
            var_declarations = []
            with open(config_json_path, "r") as file:
                var_declarations = json.load(file)["env_vars"]
            
            return var_declarations
        
        def load_var(var_declaration):
            """
            var_declaration = {var_name, param_name, default_value}
            Try to get value from os.getenv. If not possible, use the default value
            Return (param_name : param_value)
            """
            param_value = os.getenv(var_declaration["var_name"], var_declaration["default_value"])
            return (var_declaration["param_name"], param_value)
        
        var_declarations = load_var_declarations(config_json_path)
        env_vars = {}
        for var_declaration in var_declarations:
            name_value = load_var(var_declaration)
            env_vars[name_value[0]] = name_value[1]
        return env_vars
        
    
    def build(self, config_json_path, conn_to_conductor = True):
        """
        Build an instance of component service based on the given list of component services
        to include
        """
        
        print("Start building a component service based on the configuration at %s..." % config_json_path)
        """
        self_host_port and wf_host_port are two required envs. Without these declaration, 
        the service building will fail
        """
        env_vars = self.load_env_vars(config_json_path)
        self_host_port = env_vars["self_host_port"]
        wf_host_port = env_vars["wf_host_port"]
        services = self.load_services(config_json_path, wf_host_port = wf_host_port, env_vars = env_vars)
        print("Finished loading %d services..." % len(services))
        cs = ComponentService(self_host_port, wf_host_port = wf_host_port)
        for service in services:
            cs.add_resource_to_api(service.serv_type, service, env_vars)
            if conn_to_conductor:
                cs.add_conductor_worker_clients(service.serv_type, env_vars)
        print("Finished adding REST resources to the component service...")
        print("Finished adding conductor clients to the component service...")
        print("Finished building the service component. ")
        return cs