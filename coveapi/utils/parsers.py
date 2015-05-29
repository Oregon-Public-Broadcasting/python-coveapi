
try:
	# Python3 library
	from urllib.parse import urlparse
except ImportError:
	from urlparse import urlparse

from connection import (COVEAPI_HOST, COVEAPI_ROOT, COVEAPI_VERSION)

def parse_resource_uri(resource_uri):
	parse_result = urlparse(resource_uri)

	components = parse_result.path.split('/')  # components[0] == '' because of leading '/'
	if len(components) > 4:
		try:
			id = int(components[4])
		except:
			id = None
	else:
		id = None

	return {
		'root': components[1],
		'version': components[2],
		'object': components[3],
		'id': id
	}
