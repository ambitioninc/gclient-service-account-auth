import unittest

from apiclient.discovery import Resource
from httplib2 import Http
from mock import MagicMock, patch

from service_account_auth import AuthorizedService


class Test_AuthorizedService(unittest.TestCase):
    """Test the initialization of the service
    """
    @patch('service_account_auth.AuthorizedService._get_authorized_http')
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

    @patch('__builtin__.open')
    def test_returns_http_object(self, open_mock):
        open_mock.return_value.__enter__.return_value.read.return_value = 'testkeypleaseignore'
        with patch('os.environ.get') as mock_get:
            mock_get.return_value = 'private/key/location'
            http = self.mock_auth._get_authorized_http(self.mock_auth)
        self.assertIsInstance(http, Http)
