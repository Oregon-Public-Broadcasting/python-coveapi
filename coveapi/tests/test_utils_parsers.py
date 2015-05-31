import unittest

from coveapi.connection import (COVEAPI_HOST, COVEAPI_ROOT, COVEAPI_VERSION, COVEAPI_ENDPOINT_PROGRAMS)
from coveapi.utils import parsers
from tests import config

class TestUtilsParsers(unittest.TestCase):

    def test_parse_resource_uri_host_program_no_id(self):
        resource_uri = '%s/%s/%s/%s/' % (COVEAPI_HOST, COVEAPI_ROOT, COVEAPI_VERSION, COVEAPI_ENDPOINT_PROGRAMS)
        result = parsers.parse_resource_uri(resource_uri)

        self.assertEqual(COVEAPI_ROOT, result['root'])
        self.assertEqual(COVEAPI_VERSION, result['version'])
        self.assertEqual(COVEAPI_ENDPOINT_PROGRAMS, result['object'])
        self.assertEqual(None, result['id'])

    def test_parse_resource_uri_program_no_id(self):
        resource_uri = '/%s/%s/%s/' % (COVEAPI_ROOT, COVEAPI_VERSION, COVEAPI_ENDPOINT_PROGRAMS)
        result = parsers.parse_resource_uri(resource_uri)

        self.assertEqual(COVEAPI_ROOT, result['root'])
        self.assertEqual(COVEAPI_VERSION, result['version'])
        self.assertEqual(COVEAPI_ENDPOINT_PROGRAMS, result['object'])
        self.assertEqual(None, result['id'])

    def test_parse_resource_uri_program_with_id(self):
        TEST_ID = 1001
        resource_uri = '%s/%s/%s/%s/%d' % (COVEAPI_HOST, COVEAPI_ROOT, COVEAPI_VERSION, COVEAPI_ENDPOINT_PROGRAMS, TEST_ID)
        result = parsers.parse_resource_uri(resource_uri)

        self.assertEqual(COVEAPI_ROOT, result['root'])
        self.assertEqual(COVEAPI_VERSION, result['version'])
        self.assertEqual(COVEAPI_ENDPOINT_PROGRAMS, result['object'])
        self.assertEqual(TEST_ID, result['id'])


if __name__ == '__main__':
    unittest.main()