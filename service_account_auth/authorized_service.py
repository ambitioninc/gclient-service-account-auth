import os

from apiclient import discovery
from oauth2client.client import SignedJwtAssertionCredentials
import httplib2


class AuthorizedService(object):
    def __init__(self, project_id, service_name, service_version):
        """Set up the service and http objects for future requests.
        """
        self.project_id = project_id
        self.service_name = service_name
        self.auth_http = self._get_authorized_http()
        self.service = self._get_service(service_name, service_version, self.auth_http)

    def _get_service(self, service, service_version, *service_args):
        """Get the `service` object to interact with googles services.

        A "service" object is the base for all interactions with the
        API. It is created by calling `apiclient.discovery.build`
        """
        service = discovery.build(service, service_version, *service_args)
        return service

    def _get_authorized_http(self):
        """Get an http object authorized to make requests to the service.

        This http object is authorized by creating and signing a JSON Web
        Token (Jwt) with the private key of a keypair created by bigquery.

        The http object returned can be used in the `execute` methods
        of the `Request` objects that `service` objects return.
        """
        scopes = {
            'bigquery': 'https://www.googleapis.com/auth/bigquery',
            'analytics-read': 'https://www.googleapis.com/auth/analytics.readonly',
            'analytics': 'https://www.googleapis.com/auth/analytics'
        }
        service_account_email = os.environ.get('DEFAULT_SERVICE_ACCOUNT_EMAIL')
        private_key_location = os.environ.get('DEFAULT_KEY_LOCATION')
        with open(private_key_location, 'rb') as f:
            key = f.read()
        credentials = SignedJwtAssertionCredentials(
            service_account_email,
            key,
            scope=scopes[self.service_name]
        )
        http = httplib2.Http()
        http = credentials.authorize(http)
        return http
