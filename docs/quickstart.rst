.. _quickstart:

Quickstart and Basic Usage
==========================

Authorizing server to server communications with Google's APIs should
be easy. This library attempts to streamline this process. Here we
will describe all the steps needed to Authorize yourself with Google's
services and make requests to the API, without going through a
three-party oauth flow.


Creating an `AuthorizedService` object
--------------------------------------

To use the GClient Service Account libary, you must first have a
service account set up through Google's Developer Console. Before
continuing with this quickstart guide, follow Google's documentaiton
on `Creating a Service Account`_

While creating a service account take note of the following:

1. The Project-id the service account is associated with
2. The email for the service account
3. The private key for the service account

Once you have created a service account, creating an AuthorizedService
object is as simple as

.. code-block:: python

    from service_account_auth import AuthorizedService

    with open('path/to/private/key', 'rb') as f:
        private_key = f.read()

    ga_service = AuthorizedService(
        project_id='myproject-id-888'
        service_name='analytics'
        service_version='v3'
        email='my_service_account_email@developer.gserviceaccount.com'
        key=private_key
    )

In the example above, we create an AuthorizedService object for Google
Analytics. Obviously, the values for ``project_id``, ``email``, and
``key`` would need to be replaced. Once this object, ``ga_service`` is
created, all the functionallity of the Google Analytics Python API can
be accessed through the ``ga_service.service`` attribute. This
``service`` attribute is authenticated with Google, with the
authorizations associated with the service account.

.. _Creating a Service Account: https://developers.google.com/accounts/docs/OAuth2ServiceAccount#creatinganaccount

Storing the credentials
-----------------------

It is generally bad practice to store sensitive information in
code. For this reason, the GClient Service Account Auth supports
accessing sensitive information from environmant variables. Instead of
passing the email and key into ``AuthorizedService`` directly, this
information can be stored in environment variables.

If you store the service account email in the environment variable
``GCLIENT_SERVICE_ACCOUNT_EMAIL``, and a path to the private key in
the environment variable ``GCLIENT_KEY_LOCATION``, then this library
will automatically fetch the appropriate information, without you
having to include the ``email`` and ``key`` arguements for
``AuthorizedService``.

If this information is stored in environment variables, creating an
authorized service is as simple as

.. code block:: python

    from service_account_auth import AuthorizedService

    ga_service = AuthorizedService(
        'myproject-id-888', 'analytics', 'v3'
    )


Using the instance to access an API
-----------------------------------

Once you have an ``AuthorizedService`` object, you can make calls
using the python interface defined by Google's ``apiclient`` library
through the ``service`` attribute of your ``AuthorizedService``
object. For example, the `Google Analytics API`_ provides a number of
methods, one of which is the ``data`` method, which we will show an
example of calling below

.. code-block:: python

    from service_account_auth import AuthorizedService

    ga_service = AuthorizedService(
        'myproject-id-888', 'analytics', 'v3'
    )

    data = ga_service.service.data().ga().get(
        ids='ga:88888888',
        dimensions='ga:browser',
        metrics='ga:pageviews',
        start_date='2015-01-19',
        end_date='2015-01-20'
     ).execute()

The example above gets data on the number of pageviews by browser made
to our site tracked by google analytics.

Knowing what methods to call does require some knowledge of what
methods are available. For Google Analytics in particular it would be
useful to use an external libary to simplify the interface.

.. _Google Analytics API: https://github.com/google/google-api-python-client

Use with other libraries
------------------------

The `GA Grab library`_ can be used to make querying Google Analytics
much easier. 

.. _GA Grab library: https://github.com/ambitioninc/gagrab
