"""Module: `coveapi.connection`
Connection classes for accessing COVE API.
"""
try:
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
except ImportError:
    from urllib import urlencode, urlopen
    from urllib2 import Request
    
try:
    import json
except ImportError:
    import simplejson as json

from coveapi.auth import PBSAuthorization


COVEAPI_HOST = 'http://api.pbs.org'
COVEAPI_ROOT = 'cove'
COVEAPI_VERSION = 'v1'

COVEAPI_ENDPOINT_CATEGORIES = 'categories'
COVEAPI_ENDPOINT_GROUPS = 'groups'
COVEAPI_ENDPOINT_PRODUCERS = 'producers'
COVEAPI_ENDPOINT_PROGRAMS = 'programs'
COVEAPI_ENDPOINT_VIDEOS = 'videos'
COVEAPI_ENDPOINT_GRAVEYARD = 'graveyard'

class COVEAPIConnection(object):
    """Connect to the COVE API service.

    Keyword arguments:
    `api_app_id` -- your COVE API app id
    `api_app_secret` -- your COVE API secret key
    `api_host` -- host of COVE API (default: COVEAPI_HOST)
    
    Returns:
    `coveapi.connection.COVEAPIConnection` instance
    """

    def __init__(self, api_app_id, api_app_secret, api_host=COVEAPI_HOST):
        self.api_app_id = api_app_id
        self.api_app_secret = api_app_secret
        self.api_host = api_host

    def _endpoint(self, object_name):
        """
        Given an object name ('videos', 'producers', etc), return the object's endpoint.

        :param object_name: Name of the object (string) 
        :return: Requester for the object's API endpoint

        """
        endpoint = "/".join([self.api_host, COVEAPI_ROOT, COVEAPI_VERSION, object_name]) + "/"
        return Requestor(self.api_app_id, self.api_app_secret, endpoint, self.api_host)

    @property
    def programs(self, **params):
        """Handle program requests.
        
        Keyword arguments:
        `**params` -- filters, fields, sorts (see api documentation)
        
        Returns:
        `coveapi.connection.Requestor` instance
        """
        return self._endpoint(COVEAPI_ENDPOINT_PROGRAMS)
    
    @property
    def categories(self, **params):
        """Handle category requests.
        
        Keyword arguments:
        `**params` -- filters, fields, sorts (see api documentation)
        
        Returns:
        `coveapi.connection.Requestor` instance
        """
        return self._endpoint(COVEAPI_ENDPOINT_CATEGORIES)
    
    @property
    def groups(self, **params):
        """Handle group requests.
        
        Keyword arguments:
        `**params` -- filters, fields, sorts (see api documentation)
        
        Returns:
       `coveapi.connection.Requestor` instance
        """
        return self._endpoint(COVEAPI_ENDPOINT_GROUPS)

    @property
    def producers(self, **params):
        """Handle producer requests.
        
        Keyword arguments:
        `**params` -- filters, fields, sorts (see api documentation)
        
        Returns:
       `coveapi.connection.Requestor` instance
        """
        return self._endpoint(COVEAPI_ENDPOINT_PRODUCERS)

    @property
    def videos(self, **params):
        """Handle video requests.
        
        Keyword arguments:
        `**params` -- filters, fields, sorts (see api documentation)
        
        Returns:
        `coveapi.connection.Requestor` instance
        """
        return self._endpoint(COVEAPI_ENDPOINT_VIDEOS)
                         
    @property
    def graveyard(self, **params):
        """Handle graveyard requests.

        Keyword arguments:
        `**params` -- deleted_since (see api documentation)

        Returns:
        `coveapi.connection.Requestor` instance
        """
        return self._endpoint(COVEAPI_ENDPOINT_GRAVEYARD)


class Requestor(object):
    """Handle API requests.
    
    Keyword arguments:
    `api_app_id` -- your COVE API app id
    `api_app_secret` -- your COVE API secret key
    `endpoint` -- endpoint of COVE API request
    
    Returns:
    `coveapi.connection.Requestor` instance
    """
    def __init__(self, api_app_id, api_app_secret, endpoint,
                 api_host=COVEAPI_HOST):
        self.api_app_id = api_app_id
        self.api_app_secret = api_app_secret
        self.endpoint = endpoint
        self.api_host = api_host

    def get(self, resource, **params):
        """Fetch single resource from API service.

        Keyword arguments:
        `resource` -- resource id or uri
        `**params` -- filters, fields, sorts (see api documentation)
        
        Returns:
        `dict` (json)
        """
        if type(resource) == int:
            endpoint = '%s%s/' % (self.endpoint, resource)
        else:
            if resource.startswith('http://'):
                endpoint = resource
            else:
                endpoint = '%s%s' % (self.api_host, resource)
        
        return self._make_request(endpoint, params)

    def filter(self, **params):
        """Fetch resources from API service per specified parameters.

        Keyword arguments:
        `**params` -- filters, fields, sorts (see api documentation)
        
        Returns:
        `dict` (json)
        """
        return self._make_request(self.endpoint, params)
    
    def deleted_since(self, **params):
        """Fetch deleted cove assets per 'deleted_since' parm.

        Keyword arguments:
        `**params` -- datetime (see api documentation)

        Returns:
        `dict` (json)
        """
        return self._make_request(self.endpoint, params)

    def _make_request(self, endpoint, params=None):
        """Send request to COVE API and return results as json object.
        
        Keyword arguments:
        `endpoint` -- endpoint of COVE API request
        `**params` -- filters, fields, sorts (see api documentation)
        
        Returns:
        `dict` (json)
        """
        if not params:
            params = {}

        query = endpoint
        if params:
            params = list(params.items())
            params.sort()
            
            # Note: We're using urllib.urlencode() below which escapes spaces as
            # a plus ("+") since that is what the COVE API expects. But a space
            # should really be encoded as "%20" (ie. urllib.quote()). I believe
            # this is a bug in the COVE API authentication scheme... but we have
            # to live with this in the client. We'll update this to use "%20"
            # once the COVE API supports it properly.
            query = '%s?%s' % (query, urlencode(params))
        
        request = Request(query)
        
        auth = PBSAuthorization(self.api_app_id, self.api_app_secret)
        signed_request = auth.sign_request(request)

        response = urlopen(signed_request)

        return json.loads(response.read().decode('utf-8'))
