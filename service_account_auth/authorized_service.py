import os

from apiclient import discovery
from oauth2client.client import SignedJwtAssertionCredentials
import httplib2


class AuthorizedService(object):
    """Set up the service and http objects for future requests.

    Once an AuthorizedService instance is initiated, the
    AuthorizedService.service attribute will be the entrypoint for
    future calls to the google api of interest.

    :type project_id: str
    :param project_id: The id of a Google Developer Project setup
        from the `Developer Console`_. This will likely be in the
        form ``'someword-otherword-###'``.

    :type service_name: str
    :param service_name: The name of the service you want to
        connect to. For example, ``'analytics'`` for Google
        Analytics or ``'bigquery'`` for BigQuery. Currently,
        only some libaries are supported. File a github
        issue if you would like another supported.

    :type service_version: str
    :param service_version: The version of the api to connect
        to. A list of the current versions can be found on the
        list of `Google APIs for Python`_

    :type email: str (optional)
    :param email: The email for the service account
        associated with the project. To create a service account,
        see this documentation on creating `Service Account`_.
        If this argument is not provided it will be fetched using
        the :py:func:`get_email_and_key` function.

    :type key: str (optional)
    :param key: The private key for the service account. This is
        the key created during creation of the service account.
        If this argument is not provided it will be fetched using
        the :py:func:`get_email_and_key` function.

    .. _Developer Console: https://github.com/ambitioninc/django-entity/

    .. _Google APIs for Python: https://developers.google.com/api-client-library/python/apis/

    .. _Service Account: https://developers.google.com/accounts/docs/OAuth2ServiceAccount#creatinganaccount
        """
    def __init__(self, project_id, service_name, service_version, email=None, key=None):
        self.project_id = project_id
        self.service_name = service_name
        self.email, self.key = get_email_and_key(email, key)
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
            'analytics': 'https://www.googleapis.com/auth/analytics',
            'calendar': 'https://www.googleapis.com/auth/calendar'
        }
        credentials = SignedJwtAssertionCredentials(
            self.email,
            self.key,
            scope=scopes[self.service_name]
        )
        http = httplib2.Http()
        http = credentials.authorize(http)
        return http


def get_email_and_key(email=None, key=None):
    """If not passed for ``email`` or ``key`` fetch them from the
    environment.

    This function is used to dispatch the method of finding the
    service account email and associated key. If the keys are stored
    in a database, or in memory somehow, they can be passed in
    directly, and will be returned as such.

    However, if the email and key are to be fetched from the
    environment, this function will find and return them.

    The email can be stored directly in an environment
    variable. Either ``GCLIENT_SERVICE_ACCOUNT_EMAIL`` or
    ``DEFAULT_SERVICE_ACCOUNT_EMAIL``, with preference for the former.

    The key should not be stored in an environment variable directly,
    but rather a path to the file on disk should be stored, either in
    ``GCLIENT_KEY_LOCATION`` or ``DEFAULT_KEY_LOCATION``, again with
    preference for the former.

    :type email: str (optional)
    :param email: The service account email to authorize against. If
        this argument is not provided, it will be grabbed from the
        values stored in the environment variables.

    :type key: str (optional)
    :param key: A string containing the private key. If this argument
        is not provided, it will be read in from the file referenced in
        the environment variables.

    :rtype: (str, str)
    :returns: A tuple containing a service account email, and the
        associated key.
    """
    if email is None:
        standard_email = os.environ.get('GCLIENT_SERVICE_ACCOUNT_EMAIL')
        default_email = os.environ.get('DEFAULT_SERVICE_ACCOUNT_EMAIL')
        email = standard_email or default_email
    if key is None:
        standard_key = os.environ.get('GCLIENT_KEY_LOCATION')
        default_key = os.environ.get('DEFAULT_KEY_LOCATION')
        key_location = standard_key or default_key
        if key_location:
            with open(key_location, 'rb') as f:
                key = f.read()
    if key is None and email is None:
        msg = 'Email and key must be passed in or available from the environment.'
        raise ValueError(msg)
    return email, key
