from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = '\n---\nmodule: azure_rm_appgateway\nversion_added: "0.1.2"\nshort_description: Manage Application Gateway instance\ndescription:\n    - Create, update and delete instance of Application Gateway.\n\noptions:\n    resource_group:\n        description:\n            - The name of the resource group.\n        required: True\n    name:\n        description:\n            - The name of the application gateway.\n        required: True\n    location:\n        description:\n            - Resource location. If not set, location from the resource group will be used as default.\n    sku:\n        description:\n            - SKU of the application gateway resource.\n        type: dict\n        suboptions:\n            name:\n                description:\n                    - Name of an application gateway SKU.\n                choices:\n                    - \'standard_small\'\n                    - \'standard_medium\'\n                    - \'standard_large\'\n                    - \'standard_v2\'\n                    - \'waf_medium\'\n                    - \'waf_large\'\n                    - \'waf_v2\'\n            tier:\n                description:\n                    - Tier of an application gateway.\n                choices:\n                    - \'standard\'\n                    - \'standard_v2\'\n                    - \'waf\'\n                    - \'waf_v2\'\n            capacity:\n                description:\n                    - Capacity (instance count) of an application gateway.\n    ssl_policy:\n        description:\n            - SSL policy of the application gateway resource.\n        type: dict\n        suboptions:\n            disabled_ssl_protocols:\n                description:\n                    - List of SSL protocols to be disabled on application gateway.\n                type: list\n                elements: str\n                choices:\n                    - \'tls_v1_0\'\n                    - \'tls_v1_1\'\n                    - \'tls_v1_2\'\n            policy_type:\n                description:\n                    - Type of SSL Policy.\n                choices:\n                    - \'predefined\'\n                    - \'custom\'\n            policy_name:\n                description:\n                    - Name of Ssl C(predefined) policy.\n                choices:\n                    - \'ssl_policy20150501\'\n                    - \'ssl_policy20170401\'\n                    - \'ssl_policy20170401_s\'\n            cipher_suites:\n                description:\n                    - List of SSL cipher suites to be enabled in the specified order to application gateway.\n                type: list\n                elements: str\n                choices:\n                    - tls_ecdhe_rsa_with_aes_256_gcm_sha384\n                    - tls_ecdhe_rsa_with_aes_128_gcm_sha256\n                    - tls_ecdhe_rsa_with_aes_256_cbc_sha384\n                    - tls_ecdhe_rsa_with_aes_128_cbc_sha256\n                    - tls_ecdhe_rsa_with_aes_256_cbc_sha\n                    - tls_ecdhe_rsa_with_aes_128_cbc_sha\n                    - tls_dhe_rsa_with_aes_256_gcm_sha384\n                    - tls_dhe_rsa_with_aes_128_gcm_sha256\n                    - tls_dhe_rsa_with_aes_256_cbc_sha\n                    - tls_dhe_rsa_with_aes_128_cbc_sha\n                    - tls_rsa_with_aes_256_gcm_sha384\n                    - tls_rsa_with_aes_128_gcm_sha256\n                    - tls_rsa_with_aes_256_cbc_sha256\n                    - tls_rsa_with_aes_128_cbc_sha256\n                    - tls_rsa_with_aes_256_cbc_sha\n                    - tls_rsa_with_aes_128_cbc_sha\n                    - tls_ecdhe_ecdsa_with_aes_256_gcm_sha384\n                    - tls_ecdhe_ecdsa_with_aes_128_gcm_sha256\n                    - tls_ecdhe_ecdsa_with_aes_256_cbc_sha384\n                    - tls_ecdhe_ecdsa_with_aes_128_cbc_sha256\n                    - tls_ecdhe_ecdsa_with_aes_256_cbc_sha\n                    - tls_ecdhe_ecdsa_with_aes_128_cbc_sha\n                    - tls_dhe_dss_with_aes_256_cbc_sha256\n                    - tls_dhe_dss_with_aes_128_cbc_sha256\n                    - tls_dhe_dss_with_aes_256_cbc_sha\n                    - tls_dhe_dss_with_aes_128_cbc_sha\n                    - tls_rsa_with_3des_ede_cbc_sha\n                    - tls_dhe_dss_with_3des_ede_cbc_sha\n            min_protocol_version:\n                description:\n                    - Minimum version of SSL protocol to be supported on application gateway.\n                choices:\n                    - \'tls_v1_0\'\n                    - \'tls_v1_1\'\n                    - \'tls_v1_2\'\n    gateway_ip_configurations:\n        description:\n            - List of subnets used by the application gateway.\n        type: list\n        elements: dict\n        suboptions:\n            subnet:\n                description:\n                    - Reference of the subnet resource. A subnet from where application gateway gets its private address.\n                type: dict\n                suboptions:\n                    id:\n                        description:\n                            - Full ID of the subnet resource. Required if I(name) and I(virtual_network_name) are not provided.\n                    name:\n                        description:\n                            - Name of the subnet. Only used if I(virtual_network_name) is also provided.\n                    virtual_network_name:\n                        description:\n                            - Name of the virtual network. Only used if I(name) is also provided.\n            name:\n                description:\n                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.\n    authentication_certificates:\n        description:\n            - Authentication certificates of the application gateway resource.\n        type: list\n        elements: dict\n        suboptions:\n            data:\n                description:\n                    - Certificate public data - base64 encoded pfx.\n            name:\n                description:\n                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.\n    redirect_configurations:\n        description:\n            - Redirect configurations of the application gateway resource.\n        type: list\n        elements: dict\n        suboptions:\n            redirect_type:\n                description:\n                    - Redirection type.\n                choices:\n                    - \'permanent\'\n                    - \'found\'\n                    - \'see_other\'\n                    - \'temporary\'\n            target_listener:\n                description:\n                    - Reference to a listener to redirect the request to.\n            request_routing_rules:\n                description:\n                    - List of c(basic) request routing rule names within the application gateway to which the redirect is bound.\n                version_added: "1.10.0"\n            url_path_maps:\n                description:\n                    - List of URL path map names (c(path_based_routing) rules) within the application gateway to which the redirect is bound.\n                version_added: "1.10.0"\n            path_rules:\n                description:\n                    - List of URL path rules within a c(path_based_routing) rule to which the redirect is bound.\n                type: list\n                elements: dict\n                suboptions:\n                    name:\n                        description:\n                            - Name of the URL rule.\n                    path_map_name:\n                        description:\n                            - Name of URL path map.\n                version_added: "1.10.0"\n            include_path:\n                description:\n                    - Include path in the redirected url.\n            include_query_string:\n                description:\n                    - Include query string in the redirected url.\n            name:\n                description:\n                    - Name of the resource that is unique within a resource group.\n    rewrite_rule_sets:\n        description:\n            - List of rewrite configurations for the application gateway resource.\n        type: list\n        elements: dict\n        version_added: "1.11.0"\n        suboptions:\n            name:\n                description:\n                    - Name of the rewrite rule set.\n                required: True\n            rewrite_rules:\n                description:\n                    - List of rewrite rules.\n                required: True\n                type: list\n                elements: dict\n                suboptions:\n                    name:\n                        description:\n                            - Name of the rewrite rule.\n                        required: True\n                    rule_sequence:\n                        description:\n                            - Sequence of the rule that determines the order of execution within the set.\n                        required: True\n                    conditions:\n                        description:\n                            - Conditions based on which the action set execution will be evaluated.\n                        type: list\n                        elements: dict\n                        suboptions:\n                            variable:\n                                description:\n                                    - The parameter for the condition.\n                                required: True\n                            pattern:\n                                description:\n                                    - The pattern, either fixed string or regular expression, that evaluates the truthfulness of the condition.\n                                required: True\n                            ignore_case:\n                                description:\n                                    - Setting this value to true will force the pattern to do a case in-sensitive comparison.\n                                type: bool\n                                default: True\n                            negate:\n                                description:\n                                    - Setting this value to true will force to check the negation of the condition given by the user.\n                                type: bool\n                                default: False\n                    action_set:\n                        description:\n                            - Set of actions to be done as part of the rewrite rule.\n                        required: True\n                        type: dict\n                        suboptions:\n                            request_header_configurations:\n                                description:\n                                    - List of actions to be taken on request headers.\n                                type: list\n                                elements: dict\n                                suboptions:\n                                    header_name:\n                                        description:\n                                            - Name of the header.\n                                        required: True\n                                    header_value:\n                                        description:\n                                            - Value of the header.\n                                            - Leave the parameter unset to remove the header.\n                            response_header_configurations:\n                                description:\n                                    - List of actions to be taken on response headers.\n                                type: list\n                                elements: dict\n                                suboptions:\n                                    header_name:\n                                        description:\n                                            - Name of the header.\n                                        required: True\n                                    header_value:\n                                        description:\n                                            - Value of the header.\n                                            - Leave the parameter unset to remove the header.\n                            url_configuration:\n                                description:\n                                    - Action to be taken on the URL.\n                                type: dict\n                                suboptions:\n                                    modified_path:\n                                        description:\n                                            - Value to which the URL path will be rewriten.\n                                            - Leave parameter unset to keep the original URL path.\n                                    modified_query_string:\n                                        description:\n                                            - Value to which the URL query string will be rewriten.\n                                            - Leave parameter unset to keep the original URL query string.\n                                    reroute:\n                                        description:\n                                            - If set to true, will re-evaluate the path map provided in path-based request routing rules using modified path.\n                                        type: bool\n                                        default: False\n    ssl_certificates:\n        description:\n            - SSL certificates of the application gateway resource.\n        type: list\n        elements: dict\n        suboptions:\n            data:\n                description:\n                    - Base-64 encoded pfx certificate.\n                    - Only applicable in PUT Request.\n            password:\n                description:\n                    - Password for the pfx file specified in I(data).\n                    - Only applicable in PUT request.\n            name:\n                description:\n                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.\n    trusted_root_certificates:\n        version_added: "1.14.0"\n        description:\n            - Trusted Root certificates of the application gateway resource.\n        type: list\n        elements: dict\n        suboptions:\n            name:\n                description:\n                    - Name of the trusted root certificate that is unique within an Application Gateway.\n                type: str\n            data:\n                description:\n                    - Certificate public data.\n                type: str\n            key_vault_secret_id:\n                description:\n                    - Secret Id of (base-64 encoded unencrypted pfx) \'Secret\' or \'Certificate\' object stored in KeyVault.\n                type: str\n    frontend_ip_configurations:\n        description:\n            - Frontend IP addresses of the application gateway resource.\n        type: list\n        elements: dict\n        suboptions:\n            private_ip_address:\n                description:\n                    - PrivateIPAddress of the network interface IP Configuration.\n            private_ip_allocation_method:\n                description:\n                    - PrivateIP allocation method.\n                choices:\n                    - \'static\'\n                    - \'dynamic\'\n            subnet:\n                description:\n                    - Reference of the subnet resource.\n                type: dict\n                suboptions:\n                    id:\n                        description:\n                            - Full ID of the subnet resource. Required if I(name) and I(virtual_network_name) are not provided.\n                    name:\n                        description:\n                            - Name of the subnet. Only used if I(virtual_network_name) is also provided.\n                    virtual_network_name:\n                        description:\n                            - Name of the virtual network. Only used if I(name) is also provided.\n            public_ip_address:\n                description:\n                    - Reference of the PublicIP resource.\n            name:\n                description:\n                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.\n    frontend_ports:\n        description:\n            - List of frontend ports of the application gateway resource.\n        type: list\n        elements: dict\n        suboptions:\n            port:\n                description:\n                    - Frontend port.\n            name:\n                description:\n                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.\n    backend_address_pools:\n        description:\n            - List of backend address pool of the application gateway resource.\n        type: list\n        elements: dict\n        suboptions:\n            backend_addresses:\n                description:\n                    - List of backend addresses.\n                type: list\n                elements: dict\n                suboptions:\n                    fqdn:\n                        description:\n                            - Fully qualified domain name (FQDN).\n                    ip_address:\n                        description:\n                            - IP address.\n            name:\n                description:\n                    - Resource that is unique within a resource group. This name can be used to access the resource.\n    probes:\n        description:\n            - Probes available to the application gateway resource.\n        type: list\n        elements: dict\n        suboptions:\n            name:\n                description:\n                    - Name of the I(probe) that is unique within an Application Gateway.\n            protocol:\n                description:\n                    - The protocol used for the I(probe).\n                choices:\n                    - \'http\'\n                    - \'https\'\n            host:\n                description:\n                    - Host name to send the I(probe) to.\n            path:\n                description:\n                    - Relative path of I(probe).\n                    - Valid path starts from \'/\'.\n                    - Probe is sent to <Protocol>://<host>:<port><path>.\n            timeout:\n                description:\n                    - The probe timeout in seconds.\n                    - Probe marked as failed if valid response is not received with this timeout period.\n                    - Acceptable values are from 1 second to 86400 seconds.\n            interval:\n                description:\n                    - The probing interval in seconds.\n                    - This is the time interval between two consecutive probes.\n                    - Acceptable values are from 1 second to 86400 seconds.\n            unhealthy_threshold:\n                description:\n                    - The I(probe) retry count.\n                    - Backend server is marked down after consecutive probe failure count reaches UnhealthyThreshold.\n                    - Acceptable values are from 1 second to 20.\n            pick_host_name_from_backend_http_settings:\n                description:\n                    - Whether host header should be picked from the host name of the backend HTTP settings. Default value is false.\n                type: bool\n                default: False\n    backend_http_settings_collection:\n        description:\n            - Backend http settings of the application gateway resource.\n        type: list\n        elements: dict\n        suboptions:\n            probe:\n                description:\n                    - Probe resource of an application gateway.\n            port:\n                description:\n                    - The destination port on the backend.\n            protocol:\n                description:\n                    - The protocol used to communicate with the backend.\n                choices:\n                    - \'http\'\n                    - \'https\'\n            cookie_based_affinity:\n                description:\n                    - Cookie based affinity.\n                choices:\n                    - \'enabled\'\n                    - \'disabled\'\n            connection_draining:\n                version_added: "1.14.0"\n                description:\n                    - Connection draining of the backend http settings resource.\n                type: dict\n                suboptions:\n                    drain_timeout_in_sec:\n                        description:\n                            - The number of seconds connection draining is active. Acceptable values are from 1 second to 3600 seconds.\n                        type: int\n                    enabled:\n                        description:\n                            - Whether connection draining is enabled or not.\n                        type: bool\n            request_timeout:\n                description:\n                    - Request timeout in seconds.\n                    - Application Gateway will fail the request if response is not received within RequestTimeout.\n                    - Acceptable values are from 1 second to 86400 seconds.\n            authentication_certificates:\n                description:\n                    - List of references to application gateway authentication certificates.\n                    - Applicable only when C(cookie_based_affinity) is enabled, otherwise quietly ignored.\n                type: list\n                elements: dict\n                suboptions:\n                    id:\n                        description:\n                            - Resource ID.\n            trusted_root_certificates:\n                version_added: "1.14.0"\n                description:\n                    - Array of references to application gateway trusted root certificates.\n                    - Can be the name of the trusted root certificate or full resource ID.\n                type: list\n                elements: str\n            host_name:\n                description:\n                    - Host header to be sent to the backend servers.\n            pick_host_name_from_backend_address:\n                description:\n                    - Whether host header should be picked from the host name of the backend server. Default value is false.\n            affinity_cookie_name:\n                description:\n                    - Cookie name to use for the affinity cookie.\n            path:\n                description:\n                    - Path which should be used as a prefix for all C(http) requests.\n                    - Null means no path will be prefixed. Default value is null.\n            name:\n                description:\n                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.\n    http_listeners:\n        description:\n            - List of HTTP listeners of the application gateway resource.\n        type: list\n        elements: dict\n        suboptions:\n            frontend_ip_configuration:\n                description:\n                    - Frontend IP configuration resource of an application gateway.\n            frontend_port:\n                description:\n                    - Frontend port resource of an application gateway.\n            protocol:\n                description:\n                    - Protocol of the C(http) listener.\n                choices:\n                    - \'http\'\n                    - \'https\'\n            host_name:\n                description:\n                    - Host name of C(http) listener.\n            ssl_certificate:\n                description:\n                    - SSL certificate resource of an application gateway.\n            require_server_name_indication:\n                description:\n                    - Applicable only if I(protocol) is C(https). Enables SNI for multi-hosting.\n            name:\n                description:\n                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.\n    url_path_maps:\n        description:\n            - List of URL path maps of the application gateway resource.\n        type: list\n        elements: dict\n        suboptions:\n            name:\n                description:\n                    - Name of the resource that is unique within the application gateway. This name can be used to access the resource.\n            default_backend_address_pool:\n                description:\n                    - Backend address pool resource of the application gateway which will be used if no path matches occur.\n                    - Mutually exclusive with I(default_redirect_configuration).\n            default_backend_http_settings:\n                description:\n                    - Backend http settings resource of the application gateway; used with I(default_backend_address_pool).\n            default_rewrite_rule_set:\n                description:\n                    - Default rewrite rule set for the path map.\n                    - Can be the name of the rewrite rule set or full resource ID.\n                version_added: "1.11.0"\n            path_rules:\n                description:\n                    - List of URL path rules.\n                type: list\n                elements: dict\n                suboptions:\n                    name:\n                        description:\n                            - Name of the resource that is unique within the path map.\n                    backend_address_pool:\n                        description:\n                            - Backend address pool resource of the application gateway which will be used if the path is matched.\n                            - Mutually exclusive with I(redirect_configuration).\n                    backend_http_settings:\n                        description:\n                            - Backend http settings resource of the application gateway; used for the path\'s I(backend_address_pool).\n                    rewrite_rule_set:\n                        description:\n                            - Rewrite rule set for the path map.\n                            - Can be the name of the rewrite rule set or full resource ID.\n                        version_added: "1.11.0"\n                    redirect_configuration:\n                        description:\n                            - Name of redirect configuration resource of the application gateway which will be used if the path is matched.\n                            - Mutually exclusive with I(backend_address_pool).\n                        version_added: "1.10.0"\n                    paths:\n                        description:\n                            - List of paths.\n                        type: list\n                        elements: str\n            default_redirect_configuration:\n                description:\n                    - Name of redirect configuration resource of the application gateway which will be used if no path matches occur.\n                    - Mutually exclusive with I(default_backend_address_pool).\n                version_added: "1.10.0"\n    request_routing_rules:\n        description:\n            - List of request routing rules of the application gateway resource.\n        type: list\n        elements: dict\n        suboptions:\n            rule_type:\n                description:\n                    - Rule type.\n                choices:\n                    - \'basic\'\n                    - \'path_based_routing\'\n            backend_address_pool:\n                description:\n                    - Backend address pool resource of the application gateway. Not used if I(rule_type) is C(path_based_routing).\n            backend_http_settings:\n                description:\n                    - Backend C(http) settings resource of the application gateway.\n            http_listener:\n                description:\n                    - Http listener resource of the application gateway.\n            name:\n                description:\n                    - Name of the resource that is unique within a resource group. This name can be used to access the resource.\n            redirect_configuration:\n                description:\n                    - Redirect configuration resource of the application gateway.\n            url_path_map:\n                description:\n                    - URL path map resource of the application gateway. Required if I(rule_type) is C(path_based_routing).\n            rewrite_rule_set:\n                description:\n                    - Rewrite rule set for the path map.\n                    - Can be the name of the rewrite rule set or full resource ID.\n                version_added: "1.11.0"\n    autoscale_configuration:\n        version_added: "1.14.0"\n        description:\n            - Autoscale configuration of the application gateway resource.\n        type: dict\n        suboptions:\n            max_capacity:\n                description:\n                    - Upper bound on number of Application Gateway capacity.\n                type: int\n            min_capacity:\n                description:\n                    - Lower bound on number of Application Gateway capacity.\n                type: int\n    enable_http2:\n        version_added: "1.14.0"\n        description:\n            - Whether HTTP2 is enabled on the application gateway resource.\n        type: bool\n        default: False\n    web_application_firewall_configuration:\n        version_added: "1.14.0"\n        description:\n            - Web application firewall configuration of the application gateway reosurce.\n        type: dict\n        suboptions:\n            disabled_rule_groups:\n                description:\n                    - The disabled rule groups.\n                type: list\n                elements: dict\n                suboptions:\n                    rule_group_name:\n                        description:\n                            - The name of the rule group that will be disabled.\n                        type: str\n                    rules:\n                        description:\n                            - The list of rules that will be disabled. If null, all rules of the rule group will be disabled.\n                        type: list\n                        elements: int\n            enabled:\n                description:\n                    - Whether the web application firewall is enabled or not.\n                type: bool\n            exclusions:\n                description:\n                    - The exclusion list.\n                type: list\n                elements: dict\n                suboptions:\n                    match_variable:\n                        description:\n                            - The variable to be excluded.\n                        type: str\n                    selector:\n                        description:\n                            - When match_variable is a collection, operator used to specify which elements in the collection this exclusion applies to.\n                        type: str\n                    selector_match_operator:\n                        description:\n                            - When match_variable is a collection, operate on the selector to specify\n                              which elements in the collection this exclusion applies to.\n                        type: str\n            file_upload_limit_in_mb:\n                description:\n                    - Maximum file upload size in Mb for WAF.\n                type: int\n            firewall_mode:\n                description:\n                    - Web application firewall mode.\n                type: str\n                choices:\n                    - \'Detection\'\n                    - \'Prevention\'\n            max_request_body_size:\n                description:\n                    - Maximum request body size for WAF.\n                type: int\n            max_request_body_size_in_kb:\n                description:\n                    - Maximum request body size in Kb for WAF.\n                type: int\n            request_body_check:\n                description:\n                    - Whether allow WAF to check request Body.\n                type: bool\n            rule_set_type:\n                description:\n                    - The type of the web application firewall rule set.\n                    - Possible values are \'OWASP\'.\n                type: str\n                choices:\n                    - \'OWASP\'\n            rule_set_version:\n                description:\n                    - The version of the rule set type.\n                type: str\n    gateway_state:\n        description:\n            - Start or Stop the application gateway. When specified, no updates will occur to the gateway.\n        type: str\n        choices:\n            - started\n            - stopped\n    state:\n        description:\n            - Assert the state of the application gateway. Use C(present) to create or update and C(absent) to delete.\n        default: present\n        choices:\n            - absent\n            - present\n\nextends_documentation_fragment:\n    - azure.azcollection.azure\n    - azure.azcollection.azure_tags\n\nauthor:\n    - Zim Kalinowski (@zikalino)\n\n'
EXAMPLES = '\n- name: Create instance of Application Gateway\n  azure_rm_appgateway:\n    resource_group: myResourceGroup\n    name: myAppGateway\n    sku:\n      name: standard_small\n      tier: standard\n      capacity: 2\n    gateway_ip_configurations:\n      - subnet:\n          id: "{{ subnet_id }}"\n        name: app_gateway_ip_config\n    frontend_ip_configurations:\n      - subnet:\n          id: "{{ subnet_id }}"\n        name: sample_gateway_frontend_ip_config\n    frontend_ports:\n      - port: 90\n        name: ag_frontend_port\n    backend_address_pools:\n      - backend_addresses:\n          - ip_address: 10.0.0.4\n        name: test_backend_address_pool\n    backend_http_settings_collection:\n      - port: 80\n        protocol: http\n        cookie_based_affinity: enabled\n        connection_draining:\n            drain_timeout_in_sec: 60\n            enabled: true\n        name: sample_appgateway_http_settings\n    http_listeners:\n      - frontend_ip_configuration: sample_gateway_frontend_ip_config\n        frontend_port: ag_frontend_port\n        name: sample_http_listener\n    request_routing_rules:\n      - rule_type: Basic\n        backend_address_pool: test_backend_address_pool\n        backend_http_settings: sample_appgateway_http_settings\n        http_listener: sample_http_listener\n        name: rule1\n\n- name: Create instance of Application Gateway with custom trusted root certificate\n  azure_rm_appgateway:\n    resource_group: myResourceGroup\n    name: myAppGateway\n    sku:\n      name: standard_small\n      tier: standard\n      capacity: 2\n    gateway_ip_configurations:\n      - subnet:\n          id: "{{ subnet_id }}"\n        name: app_gateway_ip_config\n    frontend_ip_configurations:\n      - subnet:\n          id: "{{ subnet_id }}"\n        name: sample_gateway_frontend_ip_config\n    frontend_ports:\n      - port: 90\n        name: ag_frontend_port\n    trusted_root_certificates:\n      - name: "root_cert"\n        key_vault_secret_id: "https://kv/secret"\n    backend_address_pools:\n      - backend_addresses:\n          - ip_address: 10.0.0.4\n        name: test_backend_address_pool\n    backend_http_settings_collection:\n      - port: 80\n        protocol: http\n        cookie_based_affinity: enabled\n        connection_draining:\n            drain_timeout_in_sec: 60\n            enabled: true\n        name: sample_appgateway_http_settings\n        trusted_root_certificates:\n          - "root_cert"\n    http_listeners:\n      - frontend_ip_configuration: sample_gateway_frontend_ip_config\n        frontend_port: ag_frontend_port\n        name: sample_http_listener\n    request_routing_rules:\n      - rule_type: Basic\n        backend_address_pool: test_backend_address_pool\n        backend_http_settings: sample_appgateway_http_settings\n        http_listener: sample_http_listener\n        name: rule1\n\n- name: Create instance of Application Gateway by looking up virtual network and subnet\n  azure_rm_appgateway:\n    resource_group: myResourceGroup\n    name: myAppGateway\n    sku:\n      name: standard_small\n      tier: standard\n      capacity: 2\n    gateway_ip_configurations:\n      - subnet:\n          name: default\n          virtual_network_name: my-vnet\n        name: app_gateway_ip_config\n    frontend_ip_configurations:\n      - subnet:\n          name: default\n          virtual_network_name: my-vnet\n        name: sample_gateway_frontend_ip_config\n    frontend_ports:\n      - port: 90\n        name: ag_frontend_port\n    backend_address_pools:\n      - backend_addresses:\n          - ip_address: 10.0.0.4\n        name: test_backend_address_pool\n    backend_http_settings_collection:\n      - port: 80\n        protocol: http\n        cookie_based_affinity: enabled\n        name: sample_appgateway_http_settings\n    http_listeners:\n      - frontend_ip_configuration: sample_gateway_frontend_ip_config\n        frontend_port: ag_frontend_port\n        name: sample_http_listener\n    request_routing_rules:\n      - rule_type: Basic\n        backend_address_pool: test_backend_address_pool\n        backend_http_settings: sample_appgateway_http_settings\n        http_listener: sample_http_listener\n        name: rule1\n\n- name: Create instance of Application Gateway with path based rules\n  azure_rm_appgateway:\n    resource_group: myResourceGroup\n    name: myAppGateway\n    sku:\n      name: standard_small\n      tier: standard\n      capacity: 2\n    gateway_ip_configurations:\n      - subnet:\n          id: "{{ subnet_id }}"\n        name: app_gateway_ip_config\n    frontend_ip_configurations:\n      - subnet:\n          id: "{{ subnet_id }}"\n        name: sample_gateway_frontend_ip_config\n    frontend_ports:\n      - port: 90\n        name: ag_frontend_port\n    backend_address_pools:\n      - backend_addresses:\n          - ip_address: 10.0.0.4\n        name: test_backend_address_pool\n    backend_http_settings_collection:\n      - port: 80\n        protocol: http\n        cookie_based_affinity: enabled\n        name: sample_appgateway_http_settings\n    http_listeners:\n      - frontend_ip_configuration: sample_gateway_frontend_ip_config\n        frontend_port: ag_frontend_port\n        name: sample_http_listener\n    request_routing_rules:\n      - rule_type: path_based_routing\n        http_listener: sample_http_listener\n        name: rule1\n        url_path_map: path_mappings\n    url_path_maps:\n      - name: path_mappings\n        default_backend_address_pool: test_backend_address_pool\n        default_backend_http_settings: sample_appgateway_http_settings\n        path_rules:\n          - name: path_rules\n            backend_address_pool: test_backend_address_pool\n            backend_http_settings: sample_appgateway_http_settings\n            paths:\n              - "/abc"\n              - "/123/*"\n\n- name: Create instance of Application Gateway with complex routing and redirect rules\n  azure_rm_appgateway:\n    resource_group: myResourceGroup\n    name: myComplexAppGateway\n    sku:\n      name: standard_small\n      tier: standard\n      capacity: 2\n    ssl_policy:\n      policy_type: "predefined"\n      policy_name: "ssl_policy20170401_s"\n    ssl_certificates:\n      - name: ssl_cert\n        password: your-password\n        data: "{{ lookup(\'file\', \'certfile\') }}"\n    gateway_ip_configurations:\n      - subnet:\n          id: "{{ subnet_output.state.id }}"\n          name: app_gateway_ip_config\n    frontend_ip_configurations:\n      - subnet:\n          id: "{{ subnet_output.state.id }}"\n          name: sample_gateway_frontend_ip_config\n    frontend_ports:\n      - name: "inbound-http"\n        port: 80\n      - name: "inbound-https"\n        port: 443\n    backend_address_pools:\n      - name: test_backend_address_pool1\n        backend_addresses:\n          - ip_address: 10.0.0.1\n      - name: test_backend_address_pool2\n        backend_addresses:\n          - ip_address: 10.0.0.2\n    backend_http_settings_collection:\n      - name: "http-profile1"\n        port: 443\n        protocol: https\n        pick_host_name_from_backend_address: true\n        probe: "http-probe1"\n        cookie_based_affinity: "Disabled"\n      - name: "http-profile2"\n        port: 8080\n        protocol: http\n        pick_host_name_from_backend_address: true\n        probe: "http-probe2"\n        cookie_based_affinity: "Disabled"\n    http_listeners:\n      - name: "inbound-http"\n        protocol: "http"\n        frontend_ip_configuration: "sample_gateway_frontend_ip_config"\n        frontend_port: "inbound-http"\n      - name: "inbound-traffic1"\n        protocol: "https"\n        frontend_ip_configuration: "sample_gateway_frontend_ip_config"\n        frontend_port: "inbound-https"\n        host_name: "traffic1.example.com"\n        require_server_name_indication: true\n        ssl_certificate: "ssl_cert"\n      - name: "inbound-traffic2"\n        protocol: "https"\n        frontend_ip_configuration: "sample_gateway_frontend_ip_config"\n        frontend_port: "inbound-https"\n        host_name: "traffic2.example.com"\n        require_server_name_indication: true\n        ssl_certificate: "ssl_cert"\n    url_path_maps:\n      - name: "path_mappings"\n        default_redirect_configuration: "redirect-traffic1"\n        path_rules:\n          - name: "path_rules"\n            backend_address_pool: "test_backend_address_pool1"\n            backend_http_settings: "http-profile1"\n            paths:\n              - "/abc"\n              - "/123/*"\n    request_routing_rules:\n      - name: "app-routing1"\n        rule_type: "basic"\n        http_listener: "inbound-traffic1"\n        backend_address_pool: "test_backend_address_pool2"\n        backend_http_settings: "http-profile1"\n      - name: "app-routing2"\n        rule_type: "path_based_routing"\n        http_listener: "inbound-traffic2"\n        url_path_map: "path_mappings"\n      - name: "redirect-routing"\n        rule_type: "basic"\n        http_listener: "inbound-http"\n        redirect_configuration: "redirect-http"\n    probes:\n      - name: "http-probe1"\n        interval: 30\n        path: "/abc"\n        protocol: "https"\n        pick_host_name_from_backend_http_settings: true\n        timeout: 30\n        unhealthy_threshold: 2\n      - name: "http-probe2"\n        interval: 30\n        path: "/xyz"\n        protocol: "http"\n        pick_host_name_from_backend_http_settings: true\n        timeout: 30\n        unhealthy_threshold: 2\n    redirect_configurations:\n      - name: "redirect-http"\n        redirect_type: "permanent"\n        target_listener: "inbound-traffic1"\n        include_path: true\n        include_query_string: true\n        request_routing_rules:\n          - "redirect-routing"\n      - name: "redirect-traffic1"\n        redirect_type: "found"\n        target_listener: "inbound-traffic1"\n        include_path: true\n        include_query_string: true\n        url_path_maps:\n          - "path_mappings"\n\n- name: Create v2 instance of Application Gateway with rewrite rules\n  azure_rm_appgateway:\n    resource_group: myResourceGroup\n    name: myV2AppGateway\n    sku:\n      name: standard_v2\n      tier: standard_v2\n      capacity: 2\n    ssl_policy:\n      policy_type: predefined\n      policy_name: ssl_policy20170401_s\n    ssl_certificates:\n      - name: ssl_cert\n        password: your-password\n        data: "{{ lookup(\'file\', ssl_cert) }}"\n    gateway_ip_configurations:\n      - subnet:\n          id: "{{ subnet_output.state.id }}"\n        name: app_gateway_ip_config\n    frontend_ip_configurations:\n      - name: "public-inbound-ip"\n        public_ip_address: my-appgw-pip\n    frontend_ports:\n      - name: "inbound-http"\n        port: 80\n      - name: "inbound-https"\n        port: 443\n    backend_address_pools:\n      - name: test_backend_address_pool1\n        backend_addresses:\n          - ip_address: 10.0.0.1\n      - name: test_backend_address_pool2\n        backend_addresses:\n          - ip_address: 10.0.0.2\n    backend_http_settings_collection:\n      - name: "http-profile1"\n        port: 443\n        protocol: https\n        pick_host_name_from_backend_address: true\n        probe: "http-probe1"\n        cookie_based_affinity: "Disabled"\n      - name: "http-profile2"\n        port: 8080\n        protocol: http\n        pick_host_name_from_backend_address: true\n        probe: "http-probe2"\n        cookie_based_affinity: "Disabled"\n    http_listeners:\n      - name: "inbound-http"\n        protocol: "http"\n        frontend_ip_configuration: "public-inbound-ip"\n        frontend_port: "inbound-http"\n      - name: "inbound-traffic1"\n        protocol: "https"\n        frontend_ip_configuration: "public-inbound-ip"\n        frontend_port: "inbound-https"\n        host_name: "traffic1.example.com"\n        require_server_name_indication: true\n        ssl_certificate: "ssl_cert"\n      - name: "inbound-traffic2"\n        protocol: "https"\n        frontend_ip_configuration: "public-inbound-ip"\n        frontend_port: "inbound-https"\n        host_name: "traffic2.example.com"\n        require_server_name_indication: true\n        ssl_certificate: "ssl_cert"\n    url_path_maps:\n      - name: "path_mappings"\n        default_redirect_configuration: "redirect-traffic1"\n        default_rewrite_rule_set: "configure-headers"\n        path_rules:\n          - name: "path_rules"\n            backend_address_pool: "test_backend_address_pool1"\n            backend_http_settings: "http-profile1"\n            paths:\n              - "/abc"\n              - "/123/*"\n    request_routing_rules:\n      - name: "app-routing1"\n        rule_type: "basic"\n        http_listener: "inbound-traffic1"\n        backend_address_pool: "test_backend_address_pool2"\n        backend_http_settings: "http-profile1"\n        rewrite_rule_set: "configure-headers"\n      - name: "app-routing2"\n        rule_type: "path_based_routing"\n        http_listener: "inbound-traffic2"\n        url_path_map: "path_mappings"\n      - name: "redirect-routing"\n        rule_type: "basic"\n        http_listener: "inbound-http"\n        redirect_configuration: "redirect-http"\n    rewrite_rule_sets:\n      - name: "configure-headers"\n        rewrite_rules:\n          - name: "add-security-response-header"\n            rule_sequence: 1\n            action_set:\n              response_header_configurations:\n                - header_name: "Strict-Transport-Security"\n                  header_value: "max-age=31536000"\n          - name: "remove-backend-response-headers"\n            rule_sequence: 2\n            action_set:\n              response_header_configurations:\n                - header_name: "Server"\n                - header_name: "X-Powered-By"\n          - name: "set-custom-header-condition"\n            rule_sequence: 3\n            conditions:\n              - variable: "var_client_ip"\n                pattern: "1.1.1.1"\n              - variable: "http_req_Authorization"\n                pattern: "12345"\n                ignore_case: false\n            action_set:\n              request_header_configurations:\n                - header_name: "Foo"\n                  header_value: "Bar"\n    probes:\n        - name: "http-probe1"\n          interval: 30\n          path: "/abc"\n          protocol: "https"\n          pick_host_name_from_backend_http_settings: true\n          timeout: 30\n          unhealthy_threshold: 2\n        - name: "http-probe2"\n          interval: 30\n          path: "/xyz"\n          protocol: "http"\n          pick_host_name_from_backend_http_settings: true\n          timeout: 30\n          unhealthy_threshold: 2\n    redirect_configurations:\n      - name: "redirect-http"\n        redirect_type: "permanent"\n        target_listener: "inbound-traffic1"\n        include_path: true\n        include_query_string: true\n        request_routing_rules:\n          - "redirect-routing"\n      - name: "redirect-traffic1"\n        redirect_type: "found"\n        target_listener: "inbound-traffic1"\n        include_path: true\n        include_query_string: true\n        url_path_maps:\n          - "path_mappings"\n\n- name: Create instance of Application Gateway with autoscale configuration\n  azure_rm_appgateway:\n    resource_group: myResourceGroup\n    name: myAppGateway\n    sku:\n      name: standard_small\n      tier: standard\n    autoscale_configuration:\n      max_capacity: 2\n      min_capacity: 1\n    gateway_ip_configurations:\n      - subnet:\n          id: "{{ subnet_id }}"\n        name: app_gateway_ip_config\n    frontend_ip_configurations:\n      - subnet:\n          id: "{{ subnet_id }}"\n        name: sample_gateway_frontend_ip_config\n    frontend_ports:\n      - port: 90\n        name: ag_frontend_port\n    backend_address_pools:\n      - backend_addresses:\n          - ip_address: 10.0.0.4\n        name: test_backend_address_pool\n    backend_http_settings_collection:\n      - port: 80\n        protocol: http\n        cookie_based_affinity: enabled\n        name: sample_appgateway_http_settings\n    http_listeners:\n      - frontend_ip_configuration: sample_gateway_frontend_ip_config\n        frontend_port: ag_frontend_port\n        name: sample_http_listener\n    request_routing_rules:\n      - rule_type: Basic\n        backend_address_pool: test_backend_address_pool\n        backend_http_settings: sample_appgateway_http_settings\n        http_listener: sample_http_listener\n        name: rule1\n\n- name: Create instance of Application Gateway waf_v2 with waf configuration\n  azure_rm_appgateway:\n    resource_group: myResourceGroup\n    name: myAppGateway\n    sku:\n      name: waf_v2\n      tier: waf_v2\n      capacity: 2\n    gateway_ip_configurations:\n      - subnet:\n          id: "{{ subnet_id }}"\n        name: app_gateway_ip_config\n    frontend_ip_configurations:\n      - subnet:\n          id: "{{ subnet_id }}"\n        name: sample_gateway_frontend_ip_config\n    frontend_ports:\n      - port: 90\n        name: ag_frontend_port\n    backend_address_pools:\n      - backend_addresses:\n          - ip_address: 10.0.0.4\n        name: test_backend_address_pool\n    backend_http_settings_collection:\n      - port: 80\n        protocol: http\n        cookie_based_affinity: enabled\n        name: sample_appgateway_http_settings\n    http_listeners:\n      - frontend_ip_configuration: sample_gateway_frontend_ip_config\n        frontend_port: ag_frontend_port\n        name: sample_http_listener\n    request_routing_rules:\n      - rule_type: Basic\n        backend_address_pool: test_backend_address_pool\n        backend_http_settings: sample_appgateway_http_settings\n        http_listener: sample_http_listener\n        name: rule1\n    web_application_firewall_configuration:\n      - enabled: true\n        firewall_mode: Detection\n        rule_set_type: OWASP\n        rule_set_version: 3.0\n        request_body_check: true\n        max_request_body_size_in_kb: 128\n        file_upload_limit_in_mb: 100\n\n- name: Stop an Application Gateway instance\n  azure_rm_appgateway:\n    resource_group: myResourceGroup\n    name: myAppGateway\n    gateway_state: stopped\n\n- name: Start an Application Gateway instance\n  azure_rm_appgateway:\n    resource_group: myResourceGroup\n    name: myAppGateway\n    gateway_state: started\n'
RETURN = '\nid:\n    description:\n        - Application gateway resource ID.\n    returned: always\n    type: str\n    sample: /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.Network/applicationGateways/myAppGw\nname:\n    description:\n        - Name of application gateway.\n    returned: always\n    type: str\n    sample: myAppGw\nresource_group:\n    description:\n        - Name of resource group.\n    returned: always\n    type: str\n    sample: myResourceGroup\nlocation:\n    description:\n        - Location of application gateway.\n    returned: always\n    type: str\n    sample: centralus\noperational_state:\n    description:\n        - Operating state of application gateway.\n    returned: always\n    type: str\n    sample: Running\nprovisioning_state:\n    description:\n        - Provisioning state of application gateway.\n    returned: always\n    type: str\n    sample: Succeeded\n'
import time
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common import AzureRMModuleBase
from copy import deepcopy
from ansible.module_utils.common.dict_transformations import _snake_to_camel, dict_merge, recursive_diff
try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.core.polling import LROPoller
    from msrestazure.tools import parse_resource_id, is_valid_resource_id
except ImportError:
    pass

class Actions:
    NoAction, Create, Update, Delete, Start, Stop = range(6)
sku_spec = dict(capacity=dict(type='int'), name=dict(type='str', choices=['standard_small', 'standard_medium', 'standard_large', 'standard_v2', 'waf_medium', 'waf_large', 'waf_v2']), tier=dict(type='str', choices=['standard', 'standard_v2', 'waf', 'waf_v2']))
ssl_policy_spec = dict(disabled_ssl_protocols=dict(type='list'), policy_type=dict(type='str', choices=['predefined', 'custom']), policy_name=dict(type='str', choices=['ssl_policy20150501', 'ssl_policy20170401', 'ssl_policy20170401_s']), cipher_suites=dict(type='list'), min_protocol_version=dict(type='str', choices=['tls_v1_0', 'tls_v1_1', 'tls_v1_2']))
probe_spec = dict(host=dict(type='str'), interval=dict(type='int'), name=dict(type='str'), path=dict(type='str'), protocol=dict(type='str', choices=['http', 'https']), timeout=dict(type='int'), unhealthy_threshold=dict(type='int'), pick_host_name_from_backend_http_settings=dict(type='bool', default=False))
redirect_path_rules_spec = dict(name=dict(type='str'), path_map_name=dict(type='str'))
redirect_configuration_spec = dict(include_path=dict(type='bool'), include_query_string=dict(type='bool'), name=dict(type='str'), redirect_type=dict(type='str', choices=['permanent', 'found', 'see_other', 'temporary']), target_listener=dict(type='str'), request_routing_rules=dict(type='list', elements='str'), url_path_maps=dict(type='list', elements='str'), path_rules=dict(type='list', elements='dict', options=redirect_path_rules_spec))
rewrite_condition_spec = dict(variable=dict(type='str', required=True), pattern=dict(type='str', required=True), ignore_case=dict(type='bool', default=True), negate=dict(type='bool', default=False))
rewrite_header_configuration_spec = dict(header_name=dict(type='str', required=True), header_value=dict(type='str', default=''))
rewrite_url_configuration_spec = dict(modified_path=dict(type='str'), modified_query_string=dict(type='str'), reroute=dict(type='bool', default=False))
rewrite_action_set_spec = dict(request_header_configurations=dict(type='list', elements='dict', options=rewrite_header_configuration_spec, default=[]), response_header_configurations=dict(type='list', elements='dict', options=rewrite_header_configuration_spec, default=[]), url_configuration=dict(type='dict', options=rewrite_url_configuration_spec))
rewrite_rule_spec = dict(name=dict(type='str', required=True), rule_sequence=dict(type='int', required=True), conditions=dict(type='list', elements='dict', options=rewrite_condition_spec, default=[]), action_set=dict(type='dict', required=True, options=rewrite_action_set_spec))
rewrite_rule_set_spec = dict(name=dict(type='str', required=True), rewrite_rules=dict(type='list', elements='dict', required=True, options=rewrite_rule_spec))
path_rules_spec = dict(name=dict(type='str'), backend_address_pool=dict(type='str'), backend_http_settings=dict(type='str'), redirect_configuration=dict(type='str'), paths=dict(type='list', elements='str'), rewrite_rule_set=dict(type='str'))
url_path_maps_spec = dict(name=dict(type='str'), default_backend_address_pool=dict(type='str'), default_backend_http_settings=dict(type='str'), path_rules=dict(type='list', elements='dict', options=path_rules_spec, mutually_exclusive=[('backend_address_pool', 'redirect_configuration')], required_one_of=[('backend_address_pool', 'redirect_configuration')], required_together=[('backend_address_pool', 'backend_http_settings')]), default_redirect_configuration=dict(type='str'), default_rewrite_rule_set=dict(type='str'))
autoscale_configuration_spec = dict(max_capacity=dict(type='int'), min_capacity=dict(type='int'))
waf_configuration_exclusions_spec = dict(match_variable=dict(type='str'), selector=dict(type='str'), selector_match_operator=dict(type='str'))
waf_configuration_disabled_rule_groups_spec = dict(rule_group_name=dict(type='str'), rules=dict(type='list', elements='int', default=[]))
web_application_firewall_configuration_spec = dict(enabled=dict(type='bool'), firewall_mode=dict(type='str', choices=['Detection', 'Prevention']), rule_set_type=dict(type='str', choices=['OWASP']), rule_set_version=dict(type='str'), request_body_check=dict(type='bool'), max_request_body_size=dict(type='int'), max_request_body_size_in_kb=dict(type='int'), file_upload_limit_in_mb=dict(type='int'), exclusions=dict(type='list', elements='dict', options=waf_configuration_exclusions_spec, default=[]), disabled_rule_groups=dict(type='list', elements='dict', options=waf_configuration_disabled_rule_groups_spec, default=[]))
trusted_root_certificates_spec = dict(name=dict(type='str'), data=dict(type='str'), key_vault_secret_id=dict(type='str', default=''))

class AzureRMApplicationGateways(AzureRMModuleBase):
    """Configuration class for an Azure RM Application Gateway resource"""

    def __init__(self):
        self.module_arg_spec = dict(resource_group=dict(type='str', required=True), name=dict(type='str', required=True), location=dict(type='str'), sku=dict(type='dict', options=sku_spec), ssl_policy=dict(type='dict', options=ssl_policy_spec), gateway_ip_configurations=dict(type='list'), authentication_certificates=dict(type='list'), ssl_certificates=dict(type='list'), trusted_root_certificates=dict(type='list', elements='dict', options=trusted_root_certificates_spec), redirect_configurations=dict(type='list', elements='dict', options=redirect_configuration_spec), rewrite_rule_sets=dict(type='list', elements='dict', options=rewrite_rule_set_spec), frontend_ip_configurations=dict(type='list'), frontend_ports=dict(type='list'), backend_address_pools=dict(type='list'), backend_http_settings_collection=dict(type='list'), probes=dict(type='list', elements='dict', options=probe_spec), http_listeners=dict(type='list'), url_path_maps=dict(type='list', elements='dict', options=url_path_maps_spec, mutually_exclusive=[('default_backend_address_pool', 'default_redirect_configuration')], required_one_of=[('default_backend_address_pool', 'default_redirect_configuration')], required_together=[('default_backend_address_pool', 'default_backend_http_settings')]), request_routing_rules=dict(type='list'), autoscale_configuration=dict(type='dict', options=autoscale_configuration_spec), web_application_firewall_configuration=dict(type='dict', options=web_application_firewall_configuration_spec), enable_http2=dict(type='bool', default=False), gateway_state=dict(type='str', choices=['started', 'stopped']), state=dict(type='str', default='present', choices=['present', 'absent']))
        self.resource_group = None
        self.name = None
        self.parameters = dict()
        self.results = dict(changed=False)
        self.state = None
        self.gateway_state = None
        self.to_do = Actions.NoAction
        super(AzureRMApplicationGateways, self).__init__(derived_arg_spec=self.module_arg_spec, supports_check_mode=True, supports_tags=True)

    def exec_module(self, **kwargs):
        """Main module execution method"""
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == 'id':
                    self.parameters['id'] = kwargs[key]
                elif key == 'location':
                    self.parameters['location'] = kwargs[key]
                elif key == 'sku':
                    ev = kwargs[key]
                    if 'name' in ev:
                        if ev['name'] == 'standard_small':
                            ev['name'] = 'Standard_Small'
                        elif ev['name'] == 'standard_medium':
                            ev['name'] = 'Standard_Medium'
                        elif ev['name'] == 'standard_large':
                            ev['name'] = 'Standard_Large'
                        elif ev['name'] == 'standard_v2':
                            ev['name'] = 'Standard_v2'
                        elif ev['name'] == 'waf_medium':
                            ev['name'] = 'WAF_Medium'
                        elif ev['name'] == 'waf_large':
                            ev['name'] = 'WAF_Large'
                        elif ev['name'] == 'waf_v2':
                            ev['name'] = 'WAF_v2'
                    if 'tier' in ev:
                        if ev['tier'] == 'standard':
                            ev['tier'] = 'Standard'
                        if ev['tier'] == 'standard_v2':
                            ev['tier'] = 'Standard_v2'
                        elif ev['tier'] == 'waf':
                            ev['tier'] = 'WAF'
                        elif ev['tier'] == 'waf_v2':
                            ev['tier'] = 'WAF_v2'
                    self.parameters['sku'] = ev
                elif key == 'ssl_policy':
                    ev = kwargs[key]
                    if 'policy_type' in ev:
                        ev['policy_type'] = _snake_to_camel(ev['policy_type'], True)
                    if 'policy_name' in ev:
                        if ev['policy_name'] == 'ssl_policy20150501':
                            ev['policy_name'] = 'AppGwSslPolicy20150501'
                        elif ev['policy_name'] == 'ssl_policy20170401':
                            ev['policy_name'] = 'AppGwSslPolicy20170401'
                        elif ev['policy_name'] == 'ssl_policy20170401_s':
                            ev['policy_name'] = 'AppGwSslPolicy20170401S'
                    if 'min_protocol_version' in ev:
                        if ev['min_protocol_version'] == 'tls_v1_0':
                            ev['min_protocol_version'] = 'TLSv1_0'
                        elif ev['min_protocol_version'] == 'tls_v1_1':
                            ev['min_protocol_version'] = 'TLSv1_1'
                        elif ev['min_protocol_version'] == 'tls_v1_2':
                            ev['min_protocol_version'] = 'TLSv1_2'
                    if 'disabled_ssl_protocols' in ev:
                        protocols = ev['disabled_ssl_protocols']
                        if protocols is not None:
                            for i in range(len(protocols)):
                                if protocols[i] == 'tls_v1_0':
                                    protocols[i] = 'TLSv1_0'
                                elif protocols[i] == 'tls_v1_1':
                                    protocols[i] = 'TLSv1_1'
                                elif protocols[i] == 'tls_v1_2':
                                    protocols[i] = 'TLSv1_2'
                    if 'cipher_suites' in ev:
                        suites = ev['cipher_suites']
                        if suites is not None:
                            for i in range(len(suites)):
                                suites[i] = suites[i].upper()
                    for prop_name in ['policy_name', 'min_protocol_version', 'disabled_ssl_protocols', 'cipher_suites']:
                        if prop_name in ev and ev[prop_name] is None:
                            del ev[prop_name]
                    self.parameters['ssl_policy'] = ev
                elif key == 'gateway_ip_configurations':
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        item = ev[i]
                        if 'subnet' in item and 'name' in item['subnet'] and ('virtual_network_name' in item['subnet']):
                            id = subnet_id(self.subscription_id, kwargs['resource_group'], item['subnet']['virtual_network_name'], item['subnet']['name'])
                            item['subnet'] = {'id': id}
                    self.parameters['gateway_ip_configurations'] = kwargs[key]
                elif key == 'authentication_certificates':
                    self.parameters['authentication_certificates'] = kwargs[key]
                elif key == 'ssl_certificates':
                    self.parameters['ssl_certificates'] = kwargs[key]
                elif key == 'trusted_root_certificates':
                    self.parameters['trusted_root_certificates'] = kwargs[key]
                elif key == 'redirect_configurations':
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        item = ev[i]
                        if 'redirect_type' in item:
                            item['redirect_type'] = _snake_to_camel(item['redirect_type'], True)
                        if 'target_listener' in item:
                            id = http_listener_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], item['target_listener'])
                            item['target_listener'] = {'id': id}
                        if item['request_routing_rules']:
                            for j in range(len(item['request_routing_rules'])):
                                rule_name = item['request_routing_rules'][j]
                                id = request_routing_rule_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], rule_name)
                                item['request_routing_rules'][j] = {'id': id}
                        else:
                            del item['request_routing_rules']
                        if item['url_path_maps']:
                            for j in range(len(item['url_path_maps'])):
                                pathmap_name = item['url_path_maps'][j]
                                id = url_path_map_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], pathmap_name)
                                item['url_path_maps'][j] = {'id': id}
                        else:
                            del item['url_path_maps']
                        if item['path_rules']:
                            for j in range(len(item['path_rules'])):
                                pathrule = item['path_rules'][j]
                                if 'name' in pathrule and 'path_map_name' in pathrule:
                                    id = url_path_rule_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], pathrule['path_map_name'], pathrule['name'])
                                    item['path_rules'][j] = {'id': id}
                        else:
                            del item['path_rules']
                    self.parameters['redirect_configurations'] = ev
                elif key == 'rewrite_rule_sets':
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        ev2 = ev[i]['rewrite_rules']
                        for j in range(len(ev2)):
                            item2 = ev2[j]
                            if item2['action_set'].get('url_configuration'):
                                if not item2['action_set']['url_configuration'].get('modified_path'):
                                    del item2['action_set']['url_configuration']['modified_path']
                                if not item2['action_set']['url_configuration'].get('modified_query_string'):
                                    del item2['action_set']['url_configuration']['modified_query_string']
                            else:
                                del item2['action_set']['url_configuration']
                    self.parameters['rewrite_rule_sets'] = ev
                elif key == 'frontend_ip_configurations':
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        item = ev[i]
                        if 'private_ip_allocation_method' in item:
                            item['private_ip_allocation_method'] = _snake_to_camel(item['private_ip_allocation_method'], True)
                        if 'public_ip_address' in item:
                            id = public_ip_id(self.subscription_id, kwargs['resource_group'], item['public_ip_address'])
                            item['public_ip_address'] = {'id': id}
                        if 'subnet' in item and 'name' in item['subnet'] and ('virtual_network_name' in item['subnet']):
                            id = subnet_id(self.subscription_id, kwargs['resource_group'], item['subnet']['virtual_network_name'], item['subnet']['name'])
                            item['subnet'] = {'id': id}
                    self.parameters['frontend_ip_configurations'] = ev
                elif key == 'frontend_ports':
                    self.parameters['frontend_ports'] = kwargs[key]
                elif key == 'backend_address_pools':
                    self.parameters['backend_address_pools'] = kwargs[key]
                elif key == 'probes':
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        item = ev[i]
                        if 'protocol' in item:
                            item['protocol'] = _snake_to_camel(item['protocol'], True)
                        if 'pick_host_name_from_backend_http_settings' in item and item['pick_host_name_from_backend_http_settings'] and ('host' in item):
                            del item['host']
                    self.parameters['probes'] = ev
                elif key == 'backend_http_settings_collection':
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        item = ev[i]
                        if 'protocol' in item:
                            item['protocol'] = _snake_to_camel(item['protocol'], True)
                        if 'cookie_based_affinity' in item:
                            item['cookie_based_affinity'] = _snake_to_camel(item['cookie_based_affinity'], True)
                        if 'probe' in item:
                            id = probe_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], item['probe'])
                            item['probe'] = {'id': id}
                        if 'trusted_root_certificates' in item:
                            for j in range(len(item['trusted_root_certificates'])):
                                id = item['trusted_root_certificates'][j]
                                id = id if is_valid_resource_id(id) else trusted_root_certificate_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], id)
                                item['trusted_root_certificates'][j] = {'id': id}
                    self.parameters['backend_http_settings_collection'] = ev
                elif key == 'http_listeners':
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        item = ev[i]
                        if 'frontend_ip_configuration' in item:
                            id = frontend_ip_configuration_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], item['frontend_ip_configuration'])
                            item['frontend_ip_configuration'] = {'id': id}
                        if 'frontend_port' in item:
                            id = frontend_port_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], item['frontend_port'])
                            item['frontend_port'] = {'id': id}
                        if 'ssl_certificate' in item:
                            id = ssl_certificate_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], item['ssl_certificate'])
                            item['ssl_certificate'] = {'id': id}
                        if 'protocol' in item:
                            item['protocol'] = _snake_to_camel(item['protocol'], True)
                        ev[i] = item
                    self.parameters['http_listeners'] = ev
                elif key == 'url_path_maps':
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        item = ev[i]
                        if item['default_backend_address_pool']:
                            id = backend_address_pool_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], item['default_backend_address_pool'])
                            item['default_backend_address_pool'] = {'id': id}
                        else:
                            del item['default_backend_address_pool']
                        if item['default_backend_http_settings']:
                            id = backend_http_settings_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], item['default_backend_http_settings'])
                            item['default_backend_http_settings'] = {'id': id}
                        else:
                            del item['default_backend_http_settings']
                        if 'path_rules' in item:
                            ev2 = item['path_rules']
                            for j in range(len(ev2)):
                                item2 = ev2[j]
                                if item2['backend_address_pool']:
                                    id = backend_address_pool_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], item2['backend_address_pool'])
                                    item2['backend_address_pool'] = {'id': id}
                                else:
                                    del item2['backend_address_pool']
                                if item2['backend_http_settings']:
                                    id = backend_http_settings_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], item2['backend_http_settings'])
                                    item2['backend_http_settings'] = {'id': id}
                                else:
                                    del item2['backend_http_settings']
                                if item2['redirect_configuration']:
                                    id = redirect_configuration_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], item2['redirect_configuration'])
                                    item2['redirect_configuration'] = {'id': id}
                                else:
                                    del item2['redirect_configuration']
                                if item2['rewrite_rule_set']:
                                    id = item2['rewrite_rule_set']
                                    id = id if is_valid_resource_id(id) else rewrite_rule_set_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], id)
                                    item2['rewrite_rule_set'] = {'id': id}
                                else:
                                    del item2['rewrite_rule_set']
                                ev2[j] = item2
                        if item['default_redirect_configuration']:
                            id = redirect_configuration_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], item['default_redirect_configuration'])
                            item['default_redirect_configuration'] = {'id': id}
                        else:
                            del item['default_redirect_configuration']
                        if item['default_rewrite_rule_set']:
                            id = item['default_rewrite_rule_set']
                            id = id if is_valid_resource_id(id) else rewrite_rule_set_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], id)
                            item['default_rewrite_rule_set'] = {'id': id}
                        else:
                            del item['default_rewrite_rule_set']
                        ev[i] = item
                    self.parameters['url_path_maps'] = ev
                elif key == 'request_routing_rules':
                    ev = kwargs[key]
                    for i in range(len(ev)):
                        item = ev[i]
                        if 'rule_type' in item and item['rule_type'] == 'path_based_routing' and ('backend_address_pool' in item):
                            del item['backend_address_pool']
                        if 'backend_address_pool' in item:
                            id = backend_address_pool_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], item['backend_address_pool'])
                            item['backend_address_pool'] = {'id': id}
                        if 'backend_http_settings' in item:
                            id = backend_http_settings_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], item['backend_http_settings'])
                            item['backend_http_settings'] = {'id': id}
                        if 'http_listener' in item:
                            id = http_listener_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], item['http_listener'])
                            item['http_listener'] = {'id': id}
                        if 'protocol' in item:
                            item['protocol'] = _snake_to_camel(item['protocol'], True)
                        if 'rule_type' in item:
                            item['rule_type'] = _snake_to_camel(item['rule_type'], True)
                        if 'redirect_configuration' in item:
                            id = redirect_configuration_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], item['redirect_configuration'])
                            item['redirect_configuration'] = {'id': id}
                        if 'url_path_map' in item:
                            id = url_path_map_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], item['url_path_map'])
                            item['url_path_map'] = {'id': id}
                        if item.get('rewrite_rule_set'):
                            id = item.get('rewrite_rule_set')
                            id = id if is_valid_resource_id(id) else rewrite_rule_set_id(self.subscription_id, kwargs['resource_group'], kwargs['name'], id)
                            item['rewrite_rule_set'] = {'id': id}
                        ev[i] = item
                    self.parameters['request_routing_rules'] = ev
                elif key == 'etag':
                    self.parameters['etag'] = kwargs[key]
                elif key == 'autoscale_configuration':
                    self.parameters['autoscale_configuration'] = kwargs[key]
                elif key == 'web_application_firewall_configuration':
                    self.parameters['web_application_firewall_configuration'] = kwargs[key]
                elif key == 'enable_http2':
                    self.parameters['enable_http2'] = kwargs[key]
        response = None
        resource_group = self.get_resource_group(self.resource_group)
        if 'location' not in self.parameters:
            self.parameters['location'] = resource_group.location
        old_response = self.get_applicationgateway()
        if not old_response:
            self.log("Application Gateway instance doesn't exist")
            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log('Application Gateway instance already exists')
            if self.state == 'absent':
                self.to_do = Actions.Delete
            elif self.state == 'present':
                self.log('Need to check if Application Gateway instance has to be deleted or may be updated')
                self.to_do = Actions.Update
        if self.to_do == Actions.Update:
            if old_response['operational_state'] == 'Stopped' and self.gateway_state == 'started':
                self.to_do = Actions.Start
            elif old_response['operational_state'] == 'Running' and self.gateway_state == 'stopped':
                self.to_do = Actions.Stop
            elif old_response['operational_state'] == 'Stopped' and self.gateway_state == 'stopped' or (old_response['operational_state'] == 'Running' and self.gateway_state == 'started'):
                self.to_do = Actions.NoAction
            elif self.parameters['location'] != old_response['location'] or self.parameters['enable_http2'] != old_response['enable_http2'] or self.parameters['sku']['name'] != old_response['sku']['name'] or (self.parameters['sku']['tier'] != old_response['sku']['tier']) or (self.parameters['sku'].get('capacity', None) != old_response['sku'].get('capacity', None)) or (not compare_arrays(old_response, self.parameters, 'authentication_certificates')) or (not compare_dicts(old_response, self.parameters, 'ssl_policy')) or (not compare_arrays(old_response, self.parameters, 'gateway_ip_configurations')) or (not compare_arrays(old_response, self.parameters, 'redirect_configurations')) or (not compare_arrays(old_response, self.parameters, 'rewrite_rule_sets')) or (not compare_arrays(old_response, self.parameters, 'frontend_ip_configurations')) or (not compare_arrays(old_response, self.parameters, 'frontend_ports')) or (not compare_arrays(old_response, self.parameters, 'backend_address_pools')) or (not compare_arrays(old_response, self.parameters, 'probes')) or (not compare_arrays(old_response, self.parameters, 'backend_http_settings_collection')) or (not compare_arrays(old_response, self.parameters, 'request_routing_rules')) or (not compare_arrays(old_response, self.parameters, 'http_listeners')) or (not compare_arrays(old_response, self.parameters, 'url_path_maps')) or (not compare_arrays(old_response, self.parameters, 'trusted_root_certificates')) or (not compare_dicts(old_response, self.parameters, 'autoscale_configuration')) or (not compare_dicts(old_response, self.parameters, 'web_application_firewall_configuration')):
                self.to_do = Actions.Update
            else:
                self.to_do = Actions.NoAction
        if self.to_do == Actions.Create or self.to_do == Actions.Update:
            self.log('Need to Create / Update the Application Gateway instance')
            if self.check_mode:
                self.results['changed'] = True
                self.results['parameters'] = self.parameters
                return self.results
            response = self.create_update_applicationgateway()
            if not old_response:
                self.results['changed'] = True
            else:
                self.results['changed'] = old_response.__ne__(response)
            self.log('Creation / Update done')
        elif self.to_do == Actions.Start or self.to_do == Actions.Stop:
            self.log('Need to Start / Stop the Application Gateway instance')
            self.results['changed'] = True
            response = old_response
            if self.check_mode:
                return self.results
            elif self.to_do == Actions.Start:
                self.start_applicationgateway()
                response['operational_state'] = 'Running'
            else:
                self.stop_applicationgateway()
                response['operational_state'] = 'Stopped'
        elif self.to_do == Actions.Delete:
            self.log('Application Gateway instance deleted')
            self.results['changed'] = True
            if self.check_mode:
                return self.results
            self.delete_applicationgateway()
            while self.get_applicationgateway():
                time.sleep(20)
        else:
            self.log('Application Gateway instance unchanged')
            self.results['changed'] = False
            response = old_response
        if response:
            self.results.update(self.format_response(response))
        return self.results

    def create_update_applicationgateway(self):
        """
        Creates or updates Application Gateway with the specified configuration.

        :return: deserialized Application Gateway instance state dictionary
        """
        self.log('Creating / Updating the Application Gateway instance {0}'.format(self.name))
        try:
            response = self.network_client.application_gateways.begin_create_or_update(resource_group_name=self.resource_group, application_gateway_name=self.name, parameters=self.parameters)
            if isinstance(response, LROPoller):
                response = self.get_poller_result(response)
        except Exception as exc:
            self.log('Error attempting to create the Application Gateway instance.')
            self.fail('Error creating the Application Gateway instance: {0}'.format(str(exc)))
        return response.as_dict()

    def delete_applicationgateway(self):
        """
        Deletes specified Application Gateway instance in the specified subscription and resource group.

        :return: True
        """
        self.log('Deleting the Application Gateway instance {0}'.format(self.name))
        try:
            response = self.network_client.application_gateways.begin_delete(resource_group_name=self.resource_group, application_gateway_name=self.name)
        except Exception as e:
            self.log('Error attempting to delete the Application Gateway instance.')
            self.fail('Error deleting the Application Gateway instance: {0}'.format(str(e)))
        return True

    def get_applicationgateway(self):
        """
        Gets the properties of the specified Application Gateway.

        :return: deserialized Application Gateway instance state dictionary
        """
        self.log('Checking if the Application Gateway instance {0} is present'.format(self.name))
        found = False
        try:
            response = self.network_client.application_gateways.get(resource_group_name=self.resource_group, application_gateway_name=self.name)
            found = True
            self.log('Response : {0}'.format(response))
            self.log('Application Gateway instance : {0} found'.format(response.name))
        except ResourceNotFoundError as e:
            self.log('Did not find the Application Gateway instance.')
        if found is True:
            return response.as_dict()
        return False

    def start_applicationgateway(self):
        self.log('Starting the Application Gateway instance {0}'.format(self.name))
        try:
            response = self.network_client.application_gateways.begin_start(resource_group_name=self.resource_group, application_gateway_name=self.name)
            if isinstance(response, LROPoller):
                self.get_poller_result(response)
        except Exception as e:
            self.log('Error attempting to start the Application Gateway instance.')
            self.fail('Error starting the Application Gateway instance: {0}'.format(str(e)))

    def stop_applicationgateway(self):
        self.log('Stopping the Application Gateway instance {0}'.format(self.name))
        try:
            response = self.network_client.application_gateways.begin_stop(resource_group_name=self.resource_group, application_gateway_name=self.name)
            if isinstance(response, LROPoller):
                self.get_poller_result(response)
        except Exception as e:
            self.log('Error attempting to stop the Application Gateway instance.')
            self.fail('Error stopping the Application Gateway instance: {0}'.format(str(e)))

    def format_response(self, appgw_dict):
        id = appgw_dict.get('id')
        id_dict = parse_resource_id(id)
        d = {'id': id, 'name': appgw_dict.get('name'), 'resource_group': id_dict.get('resource_group', self.resource_group), 'location': appgw_dict.get('location'), 'operational_state': appgw_dict.get('operational_state'), 'provisioning_state': appgw_dict.get('provisioning_state')}
        return d

def public_ip_id(subscription_id, resource_group_name, name):
    """Generate the id for a frontend ip configuration"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/publicIPAddresses/{2}'.format(subscription_id, resource_group_name, name)

def frontend_ip_configuration_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a frontend ip configuration"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/frontendIPConfigurations/{3}'.format(subscription_id, resource_group_name, appgateway_name, name)

def frontend_port_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a frontend port"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/frontendPorts/{3}'.format(subscription_id, resource_group_name, appgateway_name, name)

def redirect_configuration_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a redirect configuration"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/redirectConfigurations/{3}'.format(subscription_id, resource_group_name, appgateway_name, name)

def ssl_certificate_id(subscription_id, resource_group_name, ssl_certificate_name, name):
    """Generate the id for a frontend port"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/sslCertificates/{3}'.format(subscription_id, resource_group_name, ssl_certificate_name, name)

def backend_address_pool_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for an address pool"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/backendAddressPools/{3}'.format(subscription_id, resource_group_name, appgateway_name, name)

def probe_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a probe"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/probes/{3}'.format(subscription_id, resource_group_name, appgateway_name, name)

def backend_http_settings_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a http settings"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/backendHttpSettingsCollection/{3}'.format(subscription_id, resource_group_name, appgateway_name, name)

def http_listener_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a http listener"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/httpListeners/{3}'.format(subscription_id, resource_group_name, appgateway_name, name)

def url_path_map_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a url path map"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/urlPathMaps/{3}'.format(subscription_id, resource_group_name, appgateway_name, name)

def url_path_rule_id(subscription_id, resource_group_name, appgateway_name, url_path_map_name, name):
    """Generate the id for a url path map"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/urlPathMaps/{3}/pathRules/{4}'.format(subscription_id, resource_group_name, appgateway_name, url_path_map_name, name)

def subnet_id(subscription_id, resource_group_name, virtual_network_name, name):
    """Generate the id for a subnet in a virtual network"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/virtualNetworks/{2}/subnets/{3}'.format(subscription_id, resource_group_name, virtual_network_name, name)

def ip_configuration_id(subscription_id, resource_group_name, network_interface_name, name):
    """Generate the id for a request routing rule in an application gateway"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/networkInterfaces/{2}/ipConfigurations/{3}'.format(subscription_id, resource_group_name, network_interface_name, name)

def request_routing_rule_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a request routing rule in an application gateway"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/requestRoutingRules/{3}'.format(subscription_id, resource_group_name, appgateway_name, name)

def rewrite_rule_set_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a rewrite rule set in an application gateway"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/rewriteRuleSets/{3}'.format(subscription_id, resource_group_name, appgateway_name, name)

def trusted_root_certificate_id(subscription_id, resource_group_name, appgateway_name, name):
    """Generate the id for a trusted root certificate in an application gateway"""
    return '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Network/applicationGateways/{2}/trustedRootCertificates/{3}'.format(subscription_id, resource_group_name, appgateway_name, name)

def compare_dicts(old_params, new_params, param_name):
    """Compare two dictionaries using recursive_diff method and assuming that null values coming from yaml input
    are acting like absent values"""
    oldd = old_params.get(param_name, {})
    newd = new_params.get(param_name, {})
    if oldd == {} and newd == {}:
        return True
    diffs = recursive_diff(oldd, newd)
    if diffs is None:
        return True
    else:
        actual_diffs = diffs[1]
        return all((value is None or not value for value in actual_diffs.values()))

def compare_arrays(old_params, new_params, param_name):
    """Compare two arrays, including any nested properties on elements."""
    old = old_params.get(param_name, [])
    new = new_params.get(param_name, [])
    if old == [] and new == []:
        return True
    oldd = array_to_dict(old)
    newd = array_to_dict(new)
    newd = dict_merge(oldd, newd)
    return newd == oldd

def array_to_dict(array):
    """Converts list object to dictionary object, including any nested properties on elements."""
    new = {}
    for index, item in enumerate(array):
        new[index] = deepcopy(item)
        if isinstance(item, dict):
            for nested in item:
                if isinstance(item[nested], list):
                    new[index][nested] = array_to_dict(item[nested])
    return new

def main():
    """Main execution"""
    AzureRMApplicationGateways()
if __name__ == '__main__':
    main()