"""Package: `coveapi`
A Python client for the PBS COVE API service.
"""
from coveapi.connection import COVEAPIConnection, COVEAPI_HOST

# client version
__version__ = '0.2dev'

def connect(api_app_id, api_app_secret, api_host=COVEAPI_HOST):
    """Connect to the COVE API service.

    Keyword arguments:
    `api_app_id` -- your COVE API app id
    `api_app_secret` -- your COVE API secret key
    `api_host` -- host of COVE API (default: COVEAPI_HOST)
    
    Returns:
    `coveapi.connection.COVEAPIConnection` object
    """
    
    return COVEAPIConnection(api_app_id, api_app_secret, api_host)
