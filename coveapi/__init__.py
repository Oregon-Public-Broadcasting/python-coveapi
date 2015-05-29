"""Package: `coveapi`
A Python client for the PBS COVE API service.
"""

# client version
__version__ = '0.2dev'

# coveapi constants



def connect(api_app_id, api_app_secret, api_host=COVEAPI_HOST):
    """Connect to the COVE API service.

    Keyword arguments:
    `api_app_id` -- your COVE API app id
    `api_app_secret` -- your COVE API secret key
    `api_host` -- host of COVE API (default: COVEAPI_HOST)
    
    Returns:
    `coveapi.connection.COVEAPIConnection` object
    """
    from coveapi.connection import COVEAPIConnection
    return COVEAPIConnection(api_app_id, api_app_secret, api_host)
