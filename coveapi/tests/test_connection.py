import unittest

from connection import *
from tests import config

class TestCOVEAPIConnection(unittest.TestCase):

    def test_endpoint_method(self):
        con = COVEAPIConnection(config.COVEAPI_ID_TEST, config.COVEAPI_SECRET_TEST, config.COVEAPI_HOST_TEST)
        expected_endpoint = '%s/%s/%s/%s/' % (COVEAPI_HOST, COVEAPI_ROOT, COVEAPI_VERSION, COVEAPI_ENDPOINT_PROGRAMS)
        self.assertEqual(con._endpoint(COVEAPI_ENDPOINT_PROGRAMS).endpoint, expected_endpoint)

    def test_program_list(self):
        con = COVEAPIConnection(config.COVEAPI_ID_TEST, config.COVEAPI_SECRET_TEST, config.COVEAPI_HOST_TEST)
        response = con.programs.filter()
        self.assertIn('results', response)

    # COVE doesn't have a 'producers' endpont, but I hope they do someday (hint)
    # def test_producer_list(self):
    #     con = COVEAPIConnection(config.COVEAPI_ID_TEST, config.COVEAPI_SECRET_TEST, config.COVEAPI_HOST_TEST)
    #     response = con.producers.get('/cove/v1/producers/53/')
    #     self.assertIn('results', response)

if __name__ == '__main__':
    unittest.main()