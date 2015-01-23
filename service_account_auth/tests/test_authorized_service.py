import unittest

from apiclient.discovery import Resource
from httplib2 import Http
from mock import MagicMock, patch

from service_account_auth import AuthorizedService
from service_account_auth.authorized_service import get_email_and_key


class AuthorizedServiceTest(unittest.TestCase):
    """Test the initialization of the service
    """
    @patch('service_account_auth.AuthorizedService._get_authorized_http')
    def test_init(self, get_http_mock):
        get_http_mock.return_value = Http()
        authorized_service = AuthorizedService(
            'test-proj', 'bigquery', 'v2', email='test@example.com', key='testkey'
        )
        self.assertTrue(authorized_service.service)
        self.assertTrue(authorized_service.auth_http)


class AuthorizedServiceGetServiceTest(unittest.TestCase):
    def setUp(self):
        """Pin the method to a mock object.
        """
        self.mock_auth = MagicMock()
        self.mock_auth._get_service = AuthorizedService.__dict__['_get_service']

    def test_returns_resource_object(self):
        service = self.mock_auth._get_service(self.mock_auth, 'bigquery', 'v2')
        self.assertIsInstance(service, Resource)


class AuthorizedServiceGetAuthorizedHttpTest(unittest.TestCase):
    def setUp(self):
        """Pin the method to a mock object.
        """
        self.mock_auth = MagicMock()
        self.mock_auth.service_name = 'bigquery'
        self.mock_auth.email = 'test@example.com'
        self.mock_auth.key = 'testkey'
        self.mock_auth._get_authorized_http = AuthorizedService.__dict__['_get_authorized_http']

    def test_returns_http_object(self):
        http = self.mock_auth._get_authorized_http(self.mock_auth)
        self.assertIsInstance(http, Http)


class GetEmailAndKeyTest(unittest.TestCase):
    def setUp(self):
        self.environ = 'service_account_auth.authorized_service.os.environ'

    def test_email_in_standard(self):
        dict_patch = {'GCLIENT_SERVICE_ACCOUNT_EMAIL': 'test@example.com'}
        with patch.dict(self.environ, dict_patch, clear=True):
            email, key = get_email_and_key(key='testkey')
        expected = ('test@example.com', 'testkey')
        self.assertEqual((email, key), expected)

    def test_email_in_default(self):
        dict_patch = {'DEFAULT_SERVICE_ACCOUNT_EMAIL': 'test@example.com'}
        with patch.dict(self.environ, dict_patch, clear=True):
            email, key = get_email_and_key(key='testkey')
        expected = ('test@example.com', 'testkey')
        self.assertEqual((email, key), expected)

    @patch('__builtin__.open')
    def test_key_in_standard(self, open_mock):
        open_mock.return_value.__enter__.return_value.read.return_value = 'testkey'
        dict_patch = {'GCLIENT_KEY_LOCATION': 'testkey'}
        with patch.dict(self.environ, dict_patch, clear=True):
            email, key = get_email_and_key(email='test@example.com')
        expected = ('test@example.com', 'testkey')
        self.assertEqual((email, key), expected)

    @patch('__builtin__.open')
    def test_key_in_default(self, open_mock):
        open_mock.return_value.__enter__.return_value.read.return_value = 'testkey'
        dict_patch = {'DEFAULT_KEY_LOCATION': 'testkey'}
        with patch.dict(self.environ, dict_patch, clear=True):
            email, key = get_email_and_key(email='test@example.com')
        expected = ('test@example.com', 'testkey')
        self.assertEqual((email, key), expected)

    def test_no_email_or_key(self):
        dict_patch = {}
        with patch.dict(self.environ, dict_patch, clear=True):
            with self.assertRaises(ValueError):
                email, key = get_email_and_key()
