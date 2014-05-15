import unittest

from apiclient.discovery import Resource
from httplib2 import Http
from mock import MagicMock, patch

from retention.authorized_service import AuthorizedService


class Test_AuthorizedService(unittest.TestCase):
    """Test the initialization of the service
    """
    @patch('retention.authorized_service.AuthorizedService._get_authorized_http')
    def test_init(self, get_http_mock):
        get_http_mock.return_value = Http()
        authorized_service = AuthorizedService('test-proj', 'bigquery', 'v2')
        self.assertTrue(authorized_service.service)
        self.assertTrue(authorized_service.auth_http)


class Test_AuthorizedService_get_service(unittest.TestCase):
    def setUp(self):
        """Pin the method to a mock object.
        """
        self.mock_auth = MagicMock()
        self.mock_auth._get_service = AuthorizedService.__dict__['_get_service']

    def test_returns_resource_object(self):
        service = self.mock_auth._get_service(self.mock_auth, 'bigquery', 'v2')
        self.assertIsInstance(service, Resource)


class Test_AuthorizedService_get_authorized_http(unittest.TestCase):
    def setUp(self):
        """Pin the method to a mock object.
        """
        self.mock_auth = MagicMock()
        self.mock_auth.service_name = 'bigquery'
        self.mock_auth._get_authorized_http = AuthorizedService.__dict__['_get_authorized_http']

    def test_returns_http_object(self):
        # return __init__.py as the location of the key. An empty file.
        with patch('os.environ.get') as mock_get:
            mock_get.side_effect = lambda *args: 'retention/__init__.py'
            http = self.mock_auth._get_authorized_http(self.mock_auth)
        self.assertIsInstance(http, Http)
