import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['ProfileHttpArgs', 'ProfileHttp']

@pulumi.input_type
class ProfileHttpArgs:

    def __init__(__self__, *, name: pulumi.Input[str], accept_xff: Optional[pulumi.Input[str]]=None, app_service: Optional[pulumi.Input[str]]=None, basic_auth_realm: Optional[pulumi.Input[str]]=None, defaults_from: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, encrypt_cookie_secret: Optional[pulumi.Input[str]]=None, encrypt_cookies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, fallback_host: Optional[pulumi.Input[str]]=None, fallback_status_codes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, head_erase: Optional[pulumi.Input[str]]=None, head_insert: Optional[pulumi.Input[str]]=None, insert_xforwarded_for: Optional[pulumi.Input[str]]=None, lws_separator: Optional[pulumi.Input[str]]=None, lws_width: Optional[pulumi.Input[int]]=None, oneconnect_transformations: Optional[pulumi.Input[str]]=None, proxy_type: Optional[pulumi.Input[str]]=None, redirect_rewrite: Optional[pulumi.Input[str]]=None, request_chunking: Optional[pulumi.Input[str]]=None, response_chunking: Optional[pulumi.Input[str]]=None, response_headers_permitteds: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, server_agent_name: Optional[pulumi.Input[str]]=None, tm_partition: Optional[pulumi.Input[str]]=None, via_host_name: Optional[pulumi.Input[str]]=None, via_request: Optional[pulumi.Input[str]]=None, via_response: Optional[pulumi.Input[str]]=None, xff_alternative_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a ProfileHttp resource.
        :param pulumi.Input[str] name: Specifies the name of the http profile,name of Profile should be full path. Full path is the combination of the `partition + profile name`,For example `/Common/test-http-profile`.
        :param pulumi.Input[str] accept_xff: Enables or disables trusting the client IP address, and statistics from the client IP address, based on the request's XFF (X-forwarded-for) headers, if they exist.
        :param pulumi.Input[str] app_service: The application service to which the object belongs.
        :param pulumi.Input[str] basic_auth_realm: Specifies a quoted string for the basic authentication realm. The system sends this string to a client whenever authorization fails. The default value is `none`
        :param pulumi.Input[str] defaults_from: Specifies the profile that you want to use as the parent profile. Your new profile inherits all settings and values from the parent profile specified.
        :param pulumi.Input[str] description: Specifies user-defined description.
        :param pulumi.Input[str] encrypt_cookie_secret: Type a passphrase for cookie encryption.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] encrypt_cookies: Type the cookie names for the system to encrypt.
        :param pulumi.Input[str] fallback_host: Specifies an HTTP fallback host. HTTP redirection allows you to redirect HTTP traffic to another protocol identifier, host name, port number
        :param pulumi.Input[Sequence[pulumi.Input[str]]] fallback_status_codes: Specifies one or more three-digit status codes that can be returned by an HTTP server,that should trigger a redirection to the fallback host.
        :param pulumi.Input[str] head_erase: Specifies the header string that you want to erase from an HTTP request. Default is `none`.
        :param pulumi.Input[str] head_insert: Specifies a quoted header string that you want to insert into an HTTP request.Default is `none`.
        :param pulumi.Input[str] insert_xforwarded_for: Specifies, when enabled, that the system inserts an X-Forwarded-For header in an HTTP request with the client IP address, to use with connection pooling. The default is `Disabled`.
        :param pulumi.Input[str] lws_separator: Specifies the linear white space (LWS) separator that the system inserts when a header exceeds the maximum width you
               specify in the LWS Maximum Columns setting.
        :param pulumi.Input[int] lws_width: Specifies the linear white space (LWS) separator that the system inserts when a header exceeds the maximum width you specify in the LWS Maximum Columns setting.
        :param pulumi.Input[str] oneconnect_transformations: Enables the system to perform HTTP header transformations for the purpose of  keeping server-side connections open. This feature requires configuration of a OneConnect profile
        :param pulumi.Input[str] proxy_type: Specifies the proxy mode for this profile: reverse, explicit, or transparent. The default is `reverse`.
        :param pulumi.Input[str] redirect_rewrite: Specifies whether the system rewrites the URIs that are part of HTTP redirect (3XX) responses. The default is `none`.
        :param pulumi.Input[str] request_chunking: Specifies how the system handles HTTP content that is chunked by a client. The default is `preserve`.
        :param pulumi.Input[str] response_chunking: Specifies how the system handles HTTP content that is chunked by a server. The default is `selective`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] response_headers_permitteds: Specifies headers that the BIG-IP system allows in an HTTP response.If you are specifying more than one header, separate the headers with a blank space.
        :param pulumi.Input[str] server_agent_name: Specifies the value of the Server header in responses that the BIG-IP itself generates. The default is BigIP. If no
               string is specified, then no Server header will be added to such responses
        :param pulumi.Input[str] tm_partition: Displays the administrative partition within which this profile resides.
        :param pulumi.Input[str] via_host_name: Specifies the hostname to include into Via header
        :param pulumi.Input[str] via_request: Specifies whether to append, remove, or preserve a Via header in an HTTP request
        :param pulumi.Input[str] via_response: Specifies whether to append, remove, or preserve a Via header in an HTTP request
        :param pulumi.Input[Sequence[pulumi.Input[str]]] xff_alternative_names: Specifies alternative XFF headers instead of the default X-forwarded-for header.
        """
        pulumi.set(__self__, 'name', name)
        if accept_xff is not None:
            pulumi.set(__self__, 'accept_xff', accept_xff)
        if app_service is not None:
            pulumi.set(__self__, 'app_service', app_service)
        if basic_auth_realm is not None:
            pulumi.set(__self__, 'basic_auth_realm', basic_auth_realm)
        if defaults_from is not None:
            pulumi.set(__self__, 'defaults_from', defaults_from)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if encrypt_cookie_secret is not None:
            pulumi.set(__self__, 'encrypt_cookie_secret', encrypt_cookie_secret)
        if encrypt_cookies is not None:
            pulumi.set(__self__, 'encrypt_cookies', encrypt_cookies)
        if fallback_host is not None:
            pulumi.set(__self__, 'fallback_host', fallback_host)
        if fallback_status_codes is not None:
            pulumi.set(__self__, 'fallback_status_codes', fallback_status_codes)
        if head_erase is not None:
            pulumi.set(__self__, 'head_erase', head_erase)
        if head_insert is not None:
            pulumi.set(__self__, 'head_insert', head_insert)
        if insert_xforwarded_for is not None:
            pulumi.set(__self__, 'insert_xforwarded_for', insert_xforwarded_for)
        if lws_separator is not None:
            pulumi.set(__self__, 'lws_separator', lws_separator)
        if lws_width is not None:
            pulumi.set(__self__, 'lws_width', lws_width)
        if oneconnect_transformations is not None:
            pulumi.set(__self__, 'oneconnect_transformations', oneconnect_transformations)
        if proxy_type is not None:
            pulumi.set(__self__, 'proxy_type', proxy_type)
        if redirect_rewrite is not None:
            pulumi.set(__self__, 'redirect_rewrite', redirect_rewrite)
        if request_chunking is not None:
            pulumi.set(__self__, 'request_chunking', request_chunking)
        if response_chunking is not None:
            pulumi.set(__self__, 'response_chunking', response_chunking)
        if response_headers_permitteds is not None:
            pulumi.set(__self__, 'response_headers_permitteds', response_headers_permitteds)
        if server_agent_name is not None:
            pulumi.set(__self__, 'server_agent_name', server_agent_name)
        if tm_partition is not None:
            pulumi.set(__self__, 'tm_partition', tm_partition)
        if via_host_name is not None:
            pulumi.set(__self__, 'via_host_name', via_host_name)
        if via_request is not None:
            pulumi.set(__self__, 'via_request', via_request)
        if via_response is not None:
            pulumi.set(__self__, 'via_response', via_response)
        if xff_alternative_names is not None:
            pulumi.set(__self__, 'xff_alternative_names', xff_alternative_names)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Specifies the name of the http profile,name of Profile should be full path. Full path is the combination of the `partition + profile name`,For example `/Common/test-http-profile`.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='acceptXff')
    def accept_xff(self) -> Optional[pulumi.Input[str]]:
        """
        Enables or disables trusting the client IP address, and statistics from the client IP address, based on the request's XFF (X-forwarded-for) headers, if they exist.
        """
        return pulumi.get(self, 'accept_xff')

    @accept_xff.setter
    def accept_xff(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'accept_xff', value)

    @property
    @pulumi.getter(name='appService')
    def app_service(self) -> Optional[pulumi.Input[str]]:
        """
        The application service to which the object belongs.
        """
        return pulumi.get(self, 'app_service')

    @app_service.setter
    def app_service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'app_service', value)

    @property
    @pulumi.getter(name='basicAuthRealm')
    def basic_auth_realm(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a quoted string for the basic authentication realm. The system sends this string to a client whenever authorization fails. The default value is `none`
        """
        return pulumi.get(self, 'basic_auth_realm')

    @basic_auth_realm.setter
    def basic_auth_realm(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'basic_auth_realm', value)

    @property
    @pulumi.getter(name='defaultsFrom')
    def defaults_from(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the profile that you want to use as the parent profile. Your new profile inherits all settings and values from the parent profile specified.
        """
        return pulumi.get(self, 'defaults_from')

    @defaults_from.setter
    def defaults_from(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'defaults_from', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies user-defined description.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter(name='encryptCookieSecret')
    def encrypt_cookie_secret(self) -> Optional[pulumi.Input[str]]:
        """
        Type a passphrase for cookie encryption.
        """
        return pulumi.get(self, 'encrypt_cookie_secret')

    @encrypt_cookie_secret.setter
    def encrypt_cookie_secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'encrypt_cookie_secret', value)

    @property
    @pulumi.getter(name='encryptCookies')
    def encrypt_cookies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Type the cookie names for the system to encrypt.
        """
        return pulumi.get(self, 'encrypt_cookies')

    @encrypt_cookies.setter
    def encrypt_cookies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'encrypt_cookies', value)

    @property
    @pulumi.getter(name='fallbackHost')
    def fallback_host(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies an HTTP fallback host. HTTP redirection allows you to redirect HTTP traffic to another protocol identifier, host name, port number
        """
        return pulumi.get(self, 'fallback_host')

    @fallback_host.setter
    def fallback_host(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'fallback_host', value)

    @property
    @pulumi.getter(name='fallbackStatusCodes')
    def fallback_status_codes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies one or more three-digit status codes that can be returned by an HTTP server,that should trigger a redirection to the fallback host.
        """
        return pulumi.get(self, 'fallback_status_codes')

    @fallback_status_codes.setter
    def fallback_status_codes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'fallback_status_codes', value)

    @property
    @pulumi.getter(name='headErase')
    def head_erase(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the header string that you want to erase from an HTTP request. Default is `none`.
        """
        return pulumi.get(self, 'head_erase')

    @head_erase.setter
    def head_erase(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'head_erase', value)

    @property
    @pulumi.getter(name='headInsert')
    def head_insert(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a quoted header string that you want to insert into an HTTP request.Default is `none`.
        """
        return pulumi.get(self, 'head_insert')

    @head_insert.setter
    def head_insert(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'head_insert', value)

    @property
    @pulumi.getter(name='insertXforwardedFor')
    def insert_xforwarded_for(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies, when enabled, that the system inserts an X-Forwarded-For header in an HTTP request with the client IP address, to use with connection pooling. The default is `Disabled`.
        """
        return pulumi.get(self, 'insert_xforwarded_for')

    @insert_xforwarded_for.setter
    def insert_xforwarded_for(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'insert_xforwarded_for', value)

    @property
    @pulumi.getter(name='lwsSeparator')
    def lws_separator(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the linear white space (LWS) separator that the system inserts when a header exceeds the maximum width you
        specify in the LWS Maximum Columns setting.
        """
        return pulumi.get(self, 'lws_separator')

    @lws_separator.setter
    def lws_separator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'lws_separator', value)

    @property
    @pulumi.getter(name='lwsWidth')
    def lws_width(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the linear white space (LWS) separator that the system inserts when a header exceeds the maximum width you specify in the LWS Maximum Columns setting.
        """
        return pulumi.get(self, 'lws_width')

    @lws_width.setter
    def lws_width(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'lws_width', value)

    @property
    @pulumi.getter(name='oneconnectTransformations')
    def oneconnect_transformations(self) -> Optional[pulumi.Input[str]]:
        """
        Enables the system to perform HTTP header transformations for the purpose of  keeping server-side connections open. This feature requires configuration of a OneConnect profile
        """
        return pulumi.get(self, 'oneconnect_transformations')

    @oneconnect_transformations.setter
    def oneconnect_transformations(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'oneconnect_transformations', value)

    @property
    @pulumi.getter(name='proxyType')
    def proxy_type(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the proxy mode for this profile: reverse, explicit, or transparent. The default is `reverse`.
        """
        return pulumi.get(self, 'proxy_type')

    @proxy_type.setter
    def proxy_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'proxy_type', value)

    @property
    @pulumi.getter(name='redirectRewrite')
    def redirect_rewrite(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether the system rewrites the URIs that are part of HTTP redirect (3XX) responses. The default is `none`.
        """
        return pulumi.get(self, 'redirect_rewrite')

    @redirect_rewrite.setter
    def redirect_rewrite(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'redirect_rewrite', value)

    @property
    @pulumi.getter(name='requestChunking')
    def request_chunking(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies how the system handles HTTP content that is chunked by a client. The default is `preserve`.
        """
        return pulumi.get(self, 'request_chunking')

    @request_chunking.setter
    def request_chunking(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'request_chunking', value)

    @property
    @pulumi.getter(name='responseChunking')
    def response_chunking(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies how the system handles HTTP content that is chunked by a server. The default is `selective`.
        """
        return pulumi.get(self, 'response_chunking')

    @response_chunking.setter
    def response_chunking(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'response_chunking', value)

    @property
    @pulumi.getter(name='responseHeadersPermitteds')
    def response_headers_permitteds(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies headers that the BIG-IP system allows in an HTTP response.If you are specifying more than one header, separate the headers with a blank space.
        """
        return pulumi.get(self, 'response_headers_permitteds')

    @response_headers_permitteds.setter
    def response_headers_permitteds(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'response_headers_permitteds', value)

    @property
    @pulumi.getter(name='serverAgentName')
    def server_agent_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the value of the Server header in responses that the BIG-IP itself generates. The default is BigIP. If no
        string is specified, then no Server header will be added to such responses
        """
        return pulumi.get(self, 'server_agent_name')

    @server_agent_name.setter
    def server_agent_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'server_agent_name', value)

    @property
    @pulumi.getter(name='tmPartition')
    def tm_partition(self) -> Optional[pulumi.Input[str]]:
        """
        Displays the administrative partition within which this profile resides.
        """
        return pulumi.get(self, 'tm_partition')

    @tm_partition.setter
    def tm_partition(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'tm_partition', value)

    @property
    @pulumi.getter(name='viaHostName')
    def via_host_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the hostname to include into Via header
        """
        return pulumi.get(self, 'via_host_name')

    @via_host_name.setter
    def via_host_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'via_host_name', value)

    @property
    @pulumi.getter(name='viaRequest')
    def via_request(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether to append, remove, or preserve a Via header in an HTTP request
        """
        return pulumi.get(self, 'via_request')

    @via_request.setter
    def via_request(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'via_request', value)

    @property
    @pulumi.getter(name='viaResponse')
    def via_response(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether to append, remove, or preserve a Via header in an HTTP request
        """
        return pulumi.get(self, 'via_response')

    @via_response.setter
    def via_response(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'via_response', value)

    @property
    @pulumi.getter(name='xffAlternativeNames')
    def xff_alternative_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies alternative XFF headers instead of the default X-forwarded-for header.
        """
        return pulumi.get(self, 'xff_alternative_names')

    @xff_alternative_names.setter
    def xff_alternative_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'xff_alternative_names', value)

@pulumi.input_type
class _ProfileHttpState:

    def __init__(__self__, *, accept_xff: Optional[pulumi.Input[str]]=None, app_service: Optional[pulumi.Input[str]]=None, basic_auth_realm: Optional[pulumi.Input[str]]=None, defaults_from: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, encrypt_cookie_secret: Optional[pulumi.Input[str]]=None, encrypt_cookies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, fallback_host: Optional[pulumi.Input[str]]=None, fallback_status_codes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, head_erase: Optional[pulumi.Input[str]]=None, head_insert: Optional[pulumi.Input[str]]=None, insert_xforwarded_for: Optional[pulumi.Input[str]]=None, lws_separator: Optional[pulumi.Input[str]]=None, lws_width: Optional[pulumi.Input[int]]=None, name: Optional[pulumi.Input[str]]=None, oneconnect_transformations: Optional[pulumi.Input[str]]=None, proxy_type: Optional[pulumi.Input[str]]=None, redirect_rewrite: Optional[pulumi.Input[str]]=None, request_chunking: Optional[pulumi.Input[str]]=None, response_chunking: Optional[pulumi.Input[str]]=None, response_headers_permitteds: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, server_agent_name: Optional[pulumi.Input[str]]=None, tm_partition: Optional[pulumi.Input[str]]=None, via_host_name: Optional[pulumi.Input[str]]=None, via_request: Optional[pulumi.Input[str]]=None, via_response: Optional[pulumi.Input[str]]=None, xff_alternative_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None):
        """
        Input properties used for looking up and filtering ProfileHttp resources.
        :param pulumi.Input[str] accept_xff: Enables or disables trusting the client IP address, and statistics from the client IP address, based on the request's XFF (X-forwarded-for) headers, if they exist.
        :param pulumi.Input[str] app_service: The application service to which the object belongs.
        :param pulumi.Input[str] basic_auth_realm: Specifies a quoted string for the basic authentication realm. The system sends this string to a client whenever authorization fails. The default value is `none`
        :param pulumi.Input[str] defaults_from: Specifies the profile that you want to use as the parent profile. Your new profile inherits all settings and values from the parent profile specified.
        :param pulumi.Input[str] description: Specifies user-defined description.
        :param pulumi.Input[str] encrypt_cookie_secret: Type a passphrase for cookie encryption.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] encrypt_cookies: Type the cookie names for the system to encrypt.
        :param pulumi.Input[str] fallback_host: Specifies an HTTP fallback host. HTTP redirection allows you to redirect HTTP traffic to another protocol identifier, host name, port number
        :param pulumi.Input[Sequence[pulumi.Input[str]]] fallback_status_codes: Specifies one or more three-digit status codes that can be returned by an HTTP server,that should trigger a redirection to the fallback host.
        :param pulumi.Input[str] head_erase: Specifies the header string that you want to erase from an HTTP request. Default is `none`.
        :param pulumi.Input[str] head_insert: Specifies a quoted header string that you want to insert into an HTTP request.Default is `none`.
        :param pulumi.Input[str] insert_xforwarded_for: Specifies, when enabled, that the system inserts an X-Forwarded-For header in an HTTP request with the client IP address, to use with connection pooling. The default is `Disabled`.
        :param pulumi.Input[str] lws_separator: Specifies the linear white space (LWS) separator that the system inserts when a header exceeds the maximum width you
               specify in the LWS Maximum Columns setting.
        :param pulumi.Input[int] lws_width: Specifies the linear white space (LWS) separator that the system inserts when a header exceeds the maximum width you specify in the LWS Maximum Columns setting.
        :param pulumi.Input[str] name: Specifies the name of the http profile,name of Profile should be full path. Full path is the combination of the `partition + profile name`,For example `/Common/test-http-profile`.
        :param pulumi.Input[str] oneconnect_transformations: Enables the system to perform HTTP header transformations for the purpose of  keeping server-side connections open. This feature requires configuration of a OneConnect profile
        :param pulumi.Input[str] proxy_type: Specifies the proxy mode for this profile: reverse, explicit, or transparent. The default is `reverse`.
        :param pulumi.Input[str] redirect_rewrite: Specifies whether the system rewrites the URIs that are part of HTTP redirect (3XX) responses. The default is `none`.
        :param pulumi.Input[str] request_chunking: Specifies how the system handles HTTP content that is chunked by a client. The default is `preserve`.
        :param pulumi.Input[str] response_chunking: Specifies how the system handles HTTP content that is chunked by a server. The default is `selective`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] response_headers_permitteds: Specifies headers that the BIG-IP system allows in an HTTP response.If you are specifying more than one header, separate the headers with a blank space.
        :param pulumi.Input[str] server_agent_name: Specifies the value of the Server header in responses that the BIG-IP itself generates. The default is BigIP. If no
               string is specified, then no Server header will be added to such responses
        :param pulumi.Input[str] tm_partition: Displays the administrative partition within which this profile resides.
        :param pulumi.Input[str] via_host_name: Specifies the hostname to include into Via header
        :param pulumi.Input[str] via_request: Specifies whether to append, remove, or preserve a Via header in an HTTP request
        :param pulumi.Input[str] via_response: Specifies whether to append, remove, or preserve a Via header in an HTTP request
        :param pulumi.Input[Sequence[pulumi.Input[str]]] xff_alternative_names: Specifies alternative XFF headers instead of the default X-forwarded-for header.
        """
        if accept_xff is not None:
            pulumi.set(__self__, 'accept_xff', accept_xff)
        if app_service is not None:
            pulumi.set(__self__, 'app_service', app_service)
        if basic_auth_realm is not None:
            pulumi.set(__self__, 'basic_auth_realm', basic_auth_realm)
        if defaults_from is not None:
            pulumi.set(__self__, 'defaults_from', defaults_from)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if encrypt_cookie_secret is not None:
            pulumi.set(__self__, 'encrypt_cookie_secret', encrypt_cookie_secret)
        if encrypt_cookies is not None:
            pulumi.set(__self__, 'encrypt_cookies', encrypt_cookies)
        if fallback_host is not None:
            pulumi.set(__self__, 'fallback_host', fallback_host)
        if fallback_status_codes is not None:
            pulumi.set(__self__, 'fallback_status_codes', fallback_status_codes)
        if head_erase is not None:
            pulumi.set(__self__, 'head_erase', head_erase)
        if head_insert is not None:
            pulumi.set(__self__, 'head_insert', head_insert)
        if insert_xforwarded_for is not None:
            pulumi.set(__self__, 'insert_xforwarded_for', insert_xforwarded_for)
        if lws_separator is not None:
            pulumi.set(__self__, 'lws_separator', lws_separator)
        if lws_width is not None:
            pulumi.set(__self__, 'lws_width', lws_width)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if oneconnect_transformations is not None:
            pulumi.set(__self__, 'oneconnect_transformations', oneconnect_transformations)
        if proxy_type is not None:
            pulumi.set(__self__, 'proxy_type', proxy_type)
        if redirect_rewrite is not None:
            pulumi.set(__self__, 'redirect_rewrite', redirect_rewrite)
        if request_chunking is not None:
            pulumi.set(__self__, 'request_chunking', request_chunking)
        if response_chunking is not None:
            pulumi.set(__self__, 'response_chunking', response_chunking)
        if response_headers_permitteds is not None:
            pulumi.set(__self__, 'response_headers_permitteds', response_headers_permitteds)
        if server_agent_name is not None:
            pulumi.set(__self__, 'server_agent_name', server_agent_name)
        if tm_partition is not None:
            pulumi.set(__self__, 'tm_partition', tm_partition)
        if via_host_name is not None:
            pulumi.set(__self__, 'via_host_name', via_host_name)
        if via_request is not None:
            pulumi.set(__self__, 'via_request', via_request)
        if via_response is not None:
            pulumi.set(__self__, 'via_response', via_response)
        if xff_alternative_names is not None:
            pulumi.set(__self__, 'xff_alternative_names', xff_alternative_names)

    @property
    @pulumi.getter(name='acceptXff')
    def accept_xff(self) -> Optional[pulumi.Input[str]]:
        """
        Enables or disables trusting the client IP address, and statistics from the client IP address, based on the request's XFF (X-forwarded-for) headers, if they exist.
        """
        return pulumi.get(self, 'accept_xff')

    @accept_xff.setter
    def accept_xff(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'accept_xff', value)

    @property
    @pulumi.getter(name='appService')
    def app_service(self) -> Optional[pulumi.Input[str]]:
        """
        The application service to which the object belongs.
        """
        return pulumi.get(self, 'app_service')

    @app_service.setter
    def app_service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'app_service', value)

    @property
    @pulumi.getter(name='basicAuthRealm')
    def basic_auth_realm(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a quoted string for the basic authentication realm. The system sends this string to a client whenever authorization fails. The default value is `none`
        """
        return pulumi.get(self, 'basic_auth_realm')

    @basic_auth_realm.setter
    def basic_auth_realm(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'basic_auth_realm', value)

    @property
    @pulumi.getter(name='defaultsFrom')
    def defaults_from(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the profile that you want to use as the parent profile. Your new profile inherits all settings and values from the parent profile specified.
        """
        return pulumi.get(self, 'defaults_from')

    @defaults_from.setter
    def defaults_from(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'defaults_from', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies user-defined description.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter(name='encryptCookieSecret')
    def encrypt_cookie_secret(self) -> Optional[pulumi.Input[str]]:
        """
        Type a passphrase for cookie encryption.
        """
        return pulumi.get(self, 'encrypt_cookie_secret')

    @encrypt_cookie_secret.setter
    def encrypt_cookie_secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'encrypt_cookie_secret', value)

    @property
    @pulumi.getter(name='encryptCookies')
    def encrypt_cookies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Type the cookie names for the system to encrypt.
        """
        return pulumi.get(self, 'encrypt_cookies')

    @encrypt_cookies.setter
    def encrypt_cookies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'encrypt_cookies', value)

    @property
    @pulumi.getter(name='fallbackHost')
    def fallback_host(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies an HTTP fallback host. HTTP redirection allows you to redirect HTTP traffic to another protocol identifier, host name, port number
        """
        return pulumi.get(self, 'fallback_host')

    @fallback_host.setter
    def fallback_host(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'fallback_host', value)

    @property
    @pulumi.getter(name='fallbackStatusCodes')
    def fallback_status_codes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies one or more three-digit status codes that can be returned by an HTTP server,that should trigger a redirection to the fallback host.
        """
        return pulumi.get(self, 'fallback_status_codes')

    @fallback_status_codes.setter
    def fallback_status_codes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'fallback_status_codes', value)

    @property
    @pulumi.getter(name='headErase')
    def head_erase(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the header string that you want to erase from an HTTP request. Default is `none`.
        """
        return pulumi.get(self, 'head_erase')

    @head_erase.setter
    def head_erase(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'head_erase', value)

    @property
    @pulumi.getter(name='headInsert')
    def head_insert(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a quoted header string that you want to insert into an HTTP request.Default is `none`.
        """
        return pulumi.get(self, 'head_insert')

    @head_insert.setter
    def head_insert(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'head_insert', value)

    @property
    @pulumi.getter(name='insertXforwardedFor')
    def insert_xforwarded_for(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies, when enabled, that the system inserts an X-Forwarded-For header in an HTTP request with the client IP address, to use with connection pooling. The default is `Disabled`.
        """
        return pulumi.get(self, 'insert_xforwarded_for')

    @insert_xforwarded_for.setter
    def insert_xforwarded_for(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'insert_xforwarded_for', value)

    @property
    @pulumi.getter(name='lwsSeparator')
    def lws_separator(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the linear white space (LWS) separator that the system inserts when a header exceeds the maximum width you
        specify in the LWS Maximum Columns setting.
        """
        return pulumi.get(self, 'lws_separator')

    @lws_separator.setter
    def lws_separator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'lws_separator', value)

    @property
    @pulumi.getter(name='lwsWidth')
    def lws_width(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the linear white space (LWS) separator that the system inserts when a header exceeds the maximum width you specify in the LWS Maximum Columns setting.
        """
        return pulumi.get(self, 'lws_width')

    @lws_width.setter
    def lws_width(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'lws_width', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the http profile,name of Profile should be full path. Full path is the combination of the `partition + profile name`,For example `/Common/test-http-profile`.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='oneconnectTransformations')
    def oneconnect_transformations(self) -> Optional[pulumi.Input[str]]:
        """
        Enables the system to perform HTTP header transformations for the purpose of  keeping server-side connections open. This feature requires configuration of a OneConnect profile
        """
        return pulumi.get(self, 'oneconnect_transformations')

    @oneconnect_transformations.setter
    def oneconnect_transformations(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'oneconnect_transformations', value)

    @property
    @pulumi.getter(name='proxyType')
    def proxy_type(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the proxy mode for this profile: reverse, explicit, or transparent. The default is `reverse`.
        """
        return pulumi.get(self, 'proxy_type')

    @proxy_type.setter
    def proxy_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'proxy_type', value)

    @property
    @pulumi.getter(name='redirectRewrite')
    def redirect_rewrite(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether the system rewrites the URIs that are part of HTTP redirect (3XX) responses. The default is `none`.
        """
        return pulumi.get(self, 'redirect_rewrite')

    @redirect_rewrite.setter
    def redirect_rewrite(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'redirect_rewrite', value)

    @property
    @pulumi.getter(name='requestChunking')
    def request_chunking(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies how the system handles HTTP content that is chunked by a client. The default is `preserve`.
        """
        return pulumi.get(self, 'request_chunking')

    @request_chunking.setter
    def request_chunking(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'request_chunking', value)

    @property
    @pulumi.getter(name='responseChunking')
    def response_chunking(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies how the system handles HTTP content that is chunked by a server. The default is `selective`.
        """
        return pulumi.get(self, 'response_chunking')

    @response_chunking.setter
    def response_chunking(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'response_chunking', value)

    @property
    @pulumi.getter(name='responseHeadersPermitteds')
    def response_headers_permitteds(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies headers that the BIG-IP system allows in an HTTP response.If you are specifying more than one header, separate the headers with a blank space.
        """
        return pulumi.get(self, 'response_headers_permitteds')

    @response_headers_permitteds.setter
    def response_headers_permitteds(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'response_headers_permitteds', value)

    @property
    @pulumi.getter(name='serverAgentName')
    def server_agent_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the value of the Server header in responses that the BIG-IP itself generates. The default is BigIP. If no
        string is specified, then no Server header will be added to such responses
        """
        return pulumi.get(self, 'server_agent_name')

    @server_agent_name.setter
    def server_agent_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'server_agent_name', value)

    @property
    @pulumi.getter(name='tmPartition')
    def tm_partition(self) -> Optional[pulumi.Input[str]]:
        """
        Displays the administrative partition within which this profile resides.
        """
        return pulumi.get(self, 'tm_partition')

    @tm_partition.setter
    def tm_partition(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'tm_partition', value)

    @property
    @pulumi.getter(name='viaHostName')
    def via_host_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the hostname to include into Via header
        """
        return pulumi.get(self, 'via_host_name')

    @via_host_name.setter
    def via_host_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'via_host_name', value)

    @property
    @pulumi.getter(name='viaRequest')
    def via_request(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether to append, remove, or preserve a Via header in an HTTP request
        """
        return pulumi.get(self, 'via_request')

    @via_request.setter
    def via_request(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'via_request', value)

    @property
    @pulumi.getter(name='viaResponse')
    def via_response(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether to append, remove, or preserve a Via header in an HTTP request
        """
        return pulumi.get(self, 'via_response')

    @via_response.setter
    def via_response(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'via_response', value)

    @property
    @pulumi.getter(name='xffAlternativeNames')
    def xff_alternative_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies alternative XFF headers instead of the default X-forwarded-for header.
        """
        return pulumi.get(self, 'xff_alternative_names')

    @xff_alternative_names.setter
    def xff_alternative_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'xff_alternative_names', value)

class ProfileHttp(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, accept_xff: Optional[pulumi.Input[str]]=None, app_service: Optional[pulumi.Input[str]]=None, basic_auth_realm: Optional[pulumi.Input[str]]=None, defaults_from: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, encrypt_cookie_secret: Optional[pulumi.Input[str]]=None, encrypt_cookies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, fallback_host: Optional[pulumi.Input[str]]=None, fallback_status_codes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, head_erase: Optional[pulumi.Input[str]]=None, head_insert: Optional[pulumi.Input[str]]=None, insert_xforwarded_for: Optional[pulumi.Input[str]]=None, lws_separator: Optional[pulumi.Input[str]]=None, lws_width: Optional[pulumi.Input[int]]=None, name: Optional[pulumi.Input[str]]=None, oneconnect_transformations: Optional[pulumi.Input[str]]=None, proxy_type: Optional[pulumi.Input[str]]=None, redirect_rewrite: Optional[pulumi.Input[str]]=None, request_chunking: Optional[pulumi.Input[str]]=None, response_chunking: Optional[pulumi.Input[str]]=None, response_headers_permitteds: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, server_agent_name: Optional[pulumi.Input[str]]=None, tm_partition: Optional[pulumi.Input[str]]=None, via_host_name: Optional[pulumi.Input[str]]=None, via_request: Optional[pulumi.Input[str]]=None, via_response: Optional[pulumi.Input[str]]=None, xff_alternative_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, __props__=None):
        """
        `ltm.ProfileHttp` Configures a custom profile_http for use by health checks.

        For resources should be named with their "full path". The full path is the combination of the partition + name of the resource. For example /Common/my-pool.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_f5bigip as f5bigip

        sanjose_http = f5bigip.ltm.ProfileHttp("sanjose-http",
            defaults_from="/Common/http",
            fallback_host="titanic",
            fallback_status_codes=[
                "400",
                "500",
                "300",
            ],
            name="/Common/sanjose-http")
        ```

        ## Import

        BIG-IP LTM http profiles can be imported using the `name`, e.g. bash

        ```sh
         $ pulumi import f5bigip:ltm/profileHttp:ProfileHttp test-http /Common/test-http
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accept_xff: Enables or disables trusting the client IP address, and statistics from the client IP address, based on the request's XFF (X-forwarded-for) headers, if they exist.
        :param pulumi.Input[str] app_service: The application service to which the object belongs.
        :param pulumi.Input[str] basic_auth_realm: Specifies a quoted string for the basic authentication realm. The system sends this string to a client whenever authorization fails. The default value is `none`
        :param pulumi.Input[str] defaults_from: Specifies the profile that you want to use as the parent profile. Your new profile inherits all settings and values from the parent profile specified.
        :param pulumi.Input[str] description: Specifies user-defined description.
        :param pulumi.Input[str] encrypt_cookie_secret: Type a passphrase for cookie encryption.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] encrypt_cookies: Type the cookie names for the system to encrypt.
        :param pulumi.Input[str] fallback_host: Specifies an HTTP fallback host. HTTP redirection allows you to redirect HTTP traffic to another protocol identifier, host name, port number
        :param pulumi.Input[Sequence[pulumi.Input[str]]] fallback_status_codes: Specifies one or more three-digit status codes that can be returned by an HTTP server,that should trigger a redirection to the fallback host.
        :param pulumi.Input[str] head_erase: Specifies the header string that you want to erase from an HTTP request. Default is `none`.
        :param pulumi.Input[str] head_insert: Specifies a quoted header string that you want to insert into an HTTP request.Default is `none`.
        :param pulumi.Input[str] insert_xforwarded_for: Specifies, when enabled, that the system inserts an X-Forwarded-For header in an HTTP request with the client IP address, to use with connection pooling. The default is `Disabled`.
        :param pulumi.Input[str] lws_separator: Specifies the linear white space (LWS) separator that the system inserts when a header exceeds the maximum width you
               specify in the LWS Maximum Columns setting.
        :param pulumi.Input[int] lws_width: Specifies the linear white space (LWS) separator that the system inserts when a header exceeds the maximum width you specify in the LWS Maximum Columns setting.
        :param pulumi.Input[str] name: Specifies the name of the http profile,name of Profile should be full path. Full path is the combination of the `partition + profile name`,For example `/Common/test-http-profile`.
        :param pulumi.Input[str] oneconnect_transformations: Enables the system to perform HTTP header transformations for the purpose of  keeping server-side connections open. This feature requires configuration of a OneConnect profile
        :param pulumi.Input[str] proxy_type: Specifies the proxy mode for this profile: reverse, explicit, or transparent. The default is `reverse`.
        :param pulumi.Input[str] redirect_rewrite: Specifies whether the system rewrites the URIs that are part of HTTP redirect (3XX) responses. The default is `none`.
        :param pulumi.Input[str] request_chunking: Specifies how the system handles HTTP content that is chunked by a client. The default is `preserve`.
        :param pulumi.Input[str] response_chunking: Specifies how the system handles HTTP content that is chunked by a server. The default is `selective`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] response_headers_permitteds: Specifies headers that the BIG-IP system allows in an HTTP response.If you are specifying more than one header, separate the headers with a blank space.
        :param pulumi.Input[str] server_agent_name: Specifies the value of the Server header in responses that the BIG-IP itself generates. The default is BigIP. If no
               string is specified, then no Server header will be added to such responses
        :param pulumi.Input[str] tm_partition: Displays the administrative partition within which this profile resides.
        :param pulumi.Input[str] via_host_name: Specifies the hostname to include into Via header
        :param pulumi.Input[str] via_request: Specifies whether to append, remove, or preserve a Via header in an HTTP request
        :param pulumi.Input[str] via_response: Specifies whether to append, remove, or preserve a Via header in an HTTP request
        :param pulumi.Input[Sequence[pulumi.Input[str]]] xff_alternative_names: Specifies alternative XFF headers instead of the default X-forwarded-for header.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ProfileHttpArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        `ltm.ProfileHttp` Configures a custom profile_http for use by health checks.

        For resources should be named with their "full path". The full path is the combination of the partition + name of the resource. For example /Common/my-pool.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_f5bigip as f5bigip

        sanjose_http = f5bigip.ltm.ProfileHttp("sanjose-http",
            defaults_from="/Common/http",
            fallback_host="titanic",
            fallback_status_codes=[
                "400",
                "500",
                "300",
            ],
            name="/Common/sanjose-http")
        ```

        ## Import

        BIG-IP LTM http profiles can be imported using the `name`, e.g. bash

        ```sh
         $ pulumi import f5bigip:ltm/profileHttp:ProfileHttp test-http /Common/test-http
        ```

        :param str resource_name: The name of the resource.
        :param ProfileHttpArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ProfileHttpArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, accept_xff: Optional[pulumi.Input[str]]=None, app_service: Optional[pulumi.Input[str]]=None, basic_auth_realm: Optional[pulumi.Input[str]]=None, defaults_from: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, encrypt_cookie_secret: Optional[pulumi.Input[str]]=None, encrypt_cookies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, fallback_host: Optional[pulumi.Input[str]]=None, fallback_status_codes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, head_erase: Optional[pulumi.Input[str]]=None, head_insert: Optional[pulumi.Input[str]]=None, insert_xforwarded_for: Optional[pulumi.Input[str]]=None, lws_separator: Optional[pulumi.Input[str]]=None, lws_width: Optional[pulumi.Input[int]]=None, name: Optional[pulumi.Input[str]]=None, oneconnect_transformations: Optional[pulumi.Input[str]]=None, proxy_type: Optional[pulumi.Input[str]]=None, redirect_rewrite: Optional[pulumi.Input[str]]=None, request_chunking: Optional[pulumi.Input[str]]=None, response_chunking: Optional[pulumi.Input[str]]=None, response_headers_permitteds: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, server_agent_name: Optional[pulumi.Input[str]]=None, tm_partition: Optional[pulumi.Input[str]]=None, via_host_name: Optional[pulumi.Input[str]]=None, via_request: Optional[pulumi.Input[str]]=None, via_response: Optional[pulumi.Input[str]]=None, xff_alternative_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProfileHttpArgs.__new__(ProfileHttpArgs)
            __props__.__dict__['accept_xff'] = accept_xff
            __props__.__dict__['app_service'] = app_service
            __props__.__dict__['basic_auth_realm'] = basic_auth_realm
            __props__.__dict__['defaults_from'] = defaults_from
            __props__.__dict__['description'] = description
            __props__.__dict__['encrypt_cookie_secret'] = encrypt_cookie_secret
            __props__.__dict__['encrypt_cookies'] = encrypt_cookies
            __props__.__dict__['fallback_host'] = fallback_host
            __props__.__dict__['fallback_status_codes'] = fallback_status_codes
            __props__.__dict__['head_erase'] = head_erase
            __props__.__dict__['head_insert'] = head_insert
            __props__.__dict__['insert_xforwarded_for'] = insert_xforwarded_for
            __props__.__dict__['lws_separator'] = lws_separator
            __props__.__dict__['lws_width'] = lws_width
            if name is None and (not opts.urn):
                raise TypeError("Missing required property 'name'")
            __props__.__dict__['name'] = name
            __props__.__dict__['oneconnect_transformations'] = oneconnect_transformations
            __props__.__dict__['proxy_type'] = proxy_type
            __props__.__dict__['redirect_rewrite'] = redirect_rewrite
            __props__.__dict__['request_chunking'] = request_chunking
            __props__.__dict__['response_chunking'] = response_chunking
            __props__.__dict__['response_headers_permitteds'] = response_headers_permitteds
            __props__.__dict__['server_agent_name'] = server_agent_name
            __props__.__dict__['tm_partition'] = tm_partition
            __props__.__dict__['via_host_name'] = via_host_name
            __props__.__dict__['via_request'] = via_request
            __props__.__dict__['via_response'] = via_response
            __props__.__dict__['xff_alternative_names'] = xff_alternative_names
        super(ProfileHttp, __self__).__init__('f5bigip:ltm/profileHttp:ProfileHttp', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, accept_xff: Optional[pulumi.Input[str]]=None, app_service: Optional[pulumi.Input[str]]=None, basic_auth_realm: Optional[pulumi.Input[str]]=None, defaults_from: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, encrypt_cookie_secret: Optional[pulumi.Input[str]]=None, encrypt_cookies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, fallback_host: Optional[pulumi.Input[str]]=None, fallback_status_codes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, head_erase: Optional[pulumi.Input[str]]=None, head_insert: Optional[pulumi.Input[str]]=None, insert_xforwarded_for: Optional[pulumi.Input[str]]=None, lws_separator: Optional[pulumi.Input[str]]=None, lws_width: Optional[pulumi.Input[int]]=None, name: Optional[pulumi.Input[str]]=None, oneconnect_transformations: Optional[pulumi.Input[str]]=None, proxy_type: Optional[pulumi.Input[str]]=None, redirect_rewrite: Optional[pulumi.Input[str]]=None, request_chunking: Optional[pulumi.Input[str]]=None, response_chunking: Optional[pulumi.Input[str]]=None, response_headers_permitteds: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, server_agent_name: Optional[pulumi.Input[str]]=None, tm_partition: Optional[pulumi.Input[str]]=None, via_host_name: Optional[pulumi.Input[str]]=None, via_request: Optional[pulumi.Input[str]]=None, via_response: Optional[pulumi.Input[str]]=None, xff_alternative_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None) -> 'ProfileHttp':
        """
        Get an existing ProfileHttp resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accept_xff: Enables or disables trusting the client IP address, and statistics from the client IP address, based on the request's XFF (X-forwarded-for) headers, if they exist.
        :param pulumi.Input[str] app_service: The application service to which the object belongs.
        :param pulumi.Input[str] basic_auth_realm: Specifies a quoted string for the basic authentication realm. The system sends this string to a client whenever authorization fails. The default value is `none`
        :param pulumi.Input[str] defaults_from: Specifies the profile that you want to use as the parent profile. Your new profile inherits all settings and values from the parent profile specified.
        :param pulumi.Input[str] description: Specifies user-defined description.
        :param pulumi.Input[str] encrypt_cookie_secret: Type a passphrase for cookie encryption.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] encrypt_cookies: Type the cookie names for the system to encrypt.
        :param pulumi.Input[str] fallback_host: Specifies an HTTP fallback host. HTTP redirection allows you to redirect HTTP traffic to another protocol identifier, host name, port number
        :param pulumi.Input[Sequence[pulumi.Input[str]]] fallback_status_codes: Specifies one or more three-digit status codes that can be returned by an HTTP server,that should trigger a redirection to the fallback host.
        :param pulumi.Input[str] head_erase: Specifies the header string that you want to erase from an HTTP request. Default is `none`.
        :param pulumi.Input[str] head_insert: Specifies a quoted header string that you want to insert into an HTTP request.Default is `none`.
        :param pulumi.Input[str] insert_xforwarded_for: Specifies, when enabled, that the system inserts an X-Forwarded-For header in an HTTP request with the client IP address, to use with connection pooling. The default is `Disabled`.
        :param pulumi.Input[str] lws_separator: Specifies the linear white space (LWS) separator that the system inserts when a header exceeds the maximum width you
               specify in the LWS Maximum Columns setting.
        :param pulumi.Input[int] lws_width: Specifies the linear white space (LWS) separator that the system inserts when a header exceeds the maximum width you specify in the LWS Maximum Columns setting.
        :param pulumi.Input[str] name: Specifies the name of the http profile,name of Profile should be full path. Full path is the combination of the `partition + profile name`,For example `/Common/test-http-profile`.
        :param pulumi.Input[str] oneconnect_transformations: Enables the system to perform HTTP header transformations for the purpose of  keeping server-side connections open. This feature requires configuration of a OneConnect profile
        :param pulumi.Input[str] proxy_type: Specifies the proxy mode for this profile: reverse, explicit, or transparent. The default is `reverse`.
        :param pulumi.Input[str] redirect_rewrite: Specifies whether the system rewrites the URIs that are part of HTTP redirect (3XX) responses. The default is `none`.
        :param pulumi.Input[str] request_chunking: Specifies how the system handles HTTP content that is chunked by a client. The default is `preserve`.
        :param pulumi.Input[str] response_chunking: Specifies how the system handles HTTP content that is chunked by a server. The default is `selective`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] response_headers_permitteds: Specifies headers that the BIG-IP system allows in an HTTP response.If you are specifying more than one header, separate the headers with a blank space.
        :param pulumi.Input[str] server_agent_name: Specifies the value of the Server header in responses that the BIG-IP itself generates. The default is BigIP. If no
               string is specified, then no Server header will be added to such responses
        :param pulumi.Input[str] tm_partition: Displays the administrative partition within which this profile resides.
        :param pulumi.Input[str] via_host_name: Specifies the hostname to include into Via header
        :param pulumi.Input[str] via_request: Specifies whether to append, remove, or preserve a Via header in an HTTP request
        :param pulumi.Input[str] via_response: Specifies whether to append, remove, or preserve a Via header in an HTTP request
        :param pulumi.Input[Sequence[pulumi.Input[str]]] xff_alternative_names: Specifies alternative XFF headers instead of the default X-forwarded-for header.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _ProfileHttpState.__new__(_ProfileHttpState)
        __props__.__dict__['accept_xff'] = accept_xff
        __props__.__dict__['app_service'] = app_service
        __props__.__dict__['basic_auth_realm'] = basic_auth_realm
        __props__.__dict__['defaults_from'] = defaults_from
        __props__.__dict__['description'] = description
        __props__.__dict__['encrypt_cookie_secret'] = encrypt_cookie_secret
        __props__.__dict__['encrypt_cookies'] = encrypt_cookies
        __props__.__dict__['fallback_host'] = fallback_host
        __props__.__dict__['fallback_status_codes'] = fallback_status_codes
        __props__.__dict__['head_erase'] = head_erase
        __props__.__dict__['head_insert'] = head_insert
        __props__.__dict__['insert_xforwarded_for'] = insert_xforwarded_for
        __props__.__dict__['lws_separator'] = lws_separator
        __props__.__dict__['lws_width'] = lws_width
        __props__.__dict__['name'] = name
        __props__.__dict__['oneconnect_transformations'] = oneconnect_transformations
        __props__.__dict__['proxy_type'] = proxy_type
        __props__.__dict__['redirect_rewrite'] = redirect_rewrite
        __props__.__dict__['request_chunking'] = request_chunking
        __props__.__dict__['response_chunking'] = response_chunking
        __props__.__dict__['response_headers_permitteds'] = response_headers_permitteds
        __props__.__dict__['server_agent_name'] = server_agent_name
        __props__.__dict__['tm_partition'] = tm_partition
        __props__.__dict__['via_host_name'] = via_host_name
        __props__.__dict__['via_request'] = via_request
        __props__.__dict__['via_response'] = via_response
        __props__.__dict__['xff_alternative_names'] = xff_alternative_names
        return ProfileHttp(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='acceptXff')
    def accept_xff(self) -> pulumi.Output[str]:
        """
        Enables or disables trusting the client IP address, and statistics from the client IP address, based on the request's XFF (X-forwarded-for) headers, if they exist.
        """
        return pulumi.get(self, 'accept_xff')

    @property
    @pulumi.getter(name='appService')
    def app_service(self) -> pulumi.Output[Optional[str]]:
        """
        The application service to which the object belongs.
        """
        return pulumi.get(self, 'app_service')

    @property
    @pulumi.getter(name='basicAuthRealm')
    def basic_auth_realm(self) -> pulumi.Output[str]:
        """
        Specifies a quoted string for the basic authentication realm. The system sends this string to a client whenever authorization fails. The default value is `none`
        """
        return pulumi.get(self, 'basic_auth_realm')

    @property
    @pulumi.getter(name='defaultsFrom')
    def defaults_from(self) -> pulumi.Output[str]:
        """
        Specifies the profile that you want to use as the parent profile. Your new profile inherits all settings and values from the parent profile specified.
        """
        return pulumi.get(self, 'defaults_from')

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        Specifies user-defined description.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='encryptCookieSecret')
    def encrypt_cookie_secret(self) -> pulumi.Output[Optional[str]]:
        """
        Type a passphrase for cookie encryption.
        """
        return pulumi.get(self, 'encrypt_cookie_secret')

    @property
    @pulumi.getter(name='encryptCookies')
    def encrypt_cookies(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Type the cookie names for the system to encrypt.
        """
        return pulumi.get(self, 'encrypt_cookies')

    @property
    @pulumi.getter(name='fallbackHost')
    def fallback_host(self) -> pulumi.Output[str]:
        """
        Specifies an HTTP fallback host. HTTP redirection allows you to redirect HTTP traffic to another protocol identifier, host name, port number
        """
        return pulumi.get(self, 'fallback_host')

    @property
    @pulumi.getter(name='fallbackStatusCodes')
    def fallback_status_codes(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Specifies one or more three-digit status codes that can be returned by an HTTP server,that should trigger a redirection to the fallback host.
        """
        return pulumi.get(self, 'fallback_status_codes')

    @property
    @pulumi.getter(name='headErase')
    def head_erase(self) -> pulumi.Output[str]:
        """
        Specifies the header string that you want to erase from an HTTP request. Default is `none`.
        """
        return pulumi.get(self, 'head_erase')

    @property
    @pulumi.getter(name='headInsert')
    def head_insert(self) -> pulumi.Output[str]:
        """
        Specifies a quoted header string that you want to insert into an HTTP request.Default is `none`.
        """
        return pulumi.get(self, 'head_insert')

    @property
    @pulumi.getter(name='insertXforwardedFor')
    def insert_xforwarded_for(self) -> pulumi.Output[str]:
        """
        Specifies, when enabled, that the system inserts an X-Forwarded-For header in an HTTP request with the client IP address, to use with connection pooling. The default is `Disabled`.
        """
        return pulumi.get(self, 'insert_xforwarded_for')

    @property
    @pulumi.getter(name='lwsSeparator')
    def lws_separator(self) -> pulumi.Output[str]:
        """
        Specifies the linear white space (LWS) separator that the system inserts when a header exceeds the maximum width you
        specify in the LWS Maximum Columns setting.
        """
        return pulumi.get(self, 'lws_separator')

    @property
    @pulumi.getter(name='lwsWidth')
    def lws_width(self) -> pulumi.Output[int]:
        """
        Specifies the linear white space (LWS) separator that the system inserts when a header exceeds the maximum width you specify in the LWS Maximum Columns setting.
        """
        return pulumi.get(self, 'lws_width')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the http profile,name of Profile should be full path. Full path is the combination of the `partition + profile name`,For example `/Common/test-http-profile`.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='oneconnectTransformations')
    def oneconnect_transformations(self) -> pulumi.Output[str]:
        """
        Enables the system to perform HTTP header transformations for the purpose of  keeping server-side connections open. This feature requires configuration of a OneConnect profile
        """
        return pulumi.get(self, 'oneconnect_transformations')

    @property
    @pulumi.getter(name='proxyType')
    def proxy_type(self) -> pulumi.Output[str]:
        """
        Specifies the proxy mode for this profile: reverse, explicit, or transparent. The default is `reverse`.
        """
        return pulumi.get(self, 'proxy_type')

    @property
    @pulumi.getter(name='redirectRewrite')
    def redirect_rewrite(self) -> pulumi.Output[str]:
        """
        Specifies whether the system rewrites the URIs that are part of HTTP redirect (3XX) responses. The default is `none`.
        """
        return pulumi.get(self, 'redirect_rewrite')

    @property
    @pulumi.getter(name='requestChunking')
    def request_chunking(self) -> pulumi.Output[str]:
        """
        Specifies how the system handles HTTP content that is chunked by a client. The default is `preserve`.
        """
        return pulumi.get(self, 'request_chunking')

    @property
    @pulumi.getter(name='responseChunking')
    def response_chunking(self) -> pulumi.Output[str]:
        """
        Specifies how the system handles HTTP content that is chunked by a server. The default is `selective`.
        """
        return pulumi.get(self, 'response_chunking')

    @property
    @pulumi.getter(name='responseHeadersPermitteds')
    def response_headers_permitteds(self) -> pulumi.Output[Sequence[str]]:
        """
        Specifies headers that the BIG-IP system allows in an HTTP response.If you are specifying more than one header, separate the headers with a blank space.
        """
        return pulumi.get(self, 'response_headers_permitteds')

    @property
    @pulumi.getter(name='serverAgentName')
    def server_agent_name(self) -> pulumi.Output[str]:
        """
        Specifies the value of the Server header in responses that the BIG-IP itself generates. The default is BigIP. If no
        string is specified, then no Server header will be added to such responses
        """
        return pulumi.get(self, 'server_agent_name')

    @property
    @pulumi.getter(name='tmPartition')
    def tm_partition(self) -> pulumi.Output[Optional[str]]:
        """
        Displays the administrative partition within which this profile resides.
        """
        return pulumi.get(self, 'tm_partition')

    @property
    @pulumi.getter(name='viaHostName')
    def via_host_name(self) -> pulumi.Output[str]:
        """
        Specifies the hostname to include into Via header
        """
        return pulumi.get(self, 'via_host_name')

    @property
    @pulumi.getter(name='viaRequest')
    def via_request(self) -> pulumi.Output[str]:
        """
        Specifies whether to append, remove, or preserve a Via header in an HTTP request
        """
        return pulumi.get(self, 'via_request')

    @property
    @pulumi.getter(name='viaResponse')
    def via_response(self) -> pulumi.Output[str]:
        """
        Specifies whether to append, remove, or preserve a Via header in an HTTP request
        """
        return pulumi.get(self, 'via_response')

    @property
    @pulumi.getter(name='xffAlternativeNames')
    def xff_alternative_names(self) -> pulumi.Output[Sequence[str]]:
        """
        Specifies alternative XFF headers instead of the default X-forwarded-for header.
        """
        return pulumi.get(self, 'xff_alternative_names')