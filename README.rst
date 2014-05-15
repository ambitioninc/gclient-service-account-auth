Client API Service Account Authorization
==================================================

Easily create an authorized service-object for interacting with
google's client APIs server to server.


Overview
--------------------------------------------------

Do you have a google service account, and want to be able to
programatically access google APIs without having to have a user
present to validate an OAuth2 flow?

This library makes it simple to create an authorized service object
based on three pieces of information:

1. A google "Project Id."
2. A service account email.
3. The service account's private key.

After providing these pieces of information, you will be able to make
server to server requests to any supported API.


Installation
--------------------------------------------------

.. code-block:: none

   pip install service_account_auth

Usage
--------------------------------------------------

When communicating with Google's APIs programatically, not on behalf
of a user it makes sense to sign a token with a private key, rather
than perform an OAuth flow.

To get a private key that google will accept do the following:

1. Create a project at `Developer Console`_ and note it's project-id

2. Within that project's "APIs & auth" section, enable the appropriate
   API.

3. Within that project's "APIs & auth" section, under "Credentials"
   click "Create New Client ID" and create a "Service Account."

4. Place the created service accounts "email address" in an
   environment variable on your server called
   "DEFAULT_SERVICE_ACCOUNT_EMAIL."

5. Generate a new keypair for that service account, store it on your
   server, and create a environment variable "DEFAULT_KEY_LOCATION"
   containing a path to that key.

Once the steps above are complete, it's simple to create an authorized
service object that can access a given API:

.. code-block:: python

   from service_account_auth import AuthorizedService

   my_analytics_service = AuthorizedService(
       project_id='my-projectid-555',
       service_name='analytics',
       service_version='v3'
   )

The code above will create an authorized service object which can be
used to access google analytics API endpoints:

.. code-block:: python

   s = my_analytics_service.service
   analytics_account_list = s.management().accounts().list().execute()

Likewise, by varying the ``service_name`` and ``service_version``
arguments, you can access any available API with the same format and
credentials.

.. _Developer Console: https://console.developers.google.com/

Supported Services
--------------------------------------------------

Google provides python client libraries for many of its APIs. This
library can create authorized service objects for the following APIs:

- BigQuery
- Analytics

For many of those not listed here, suport is as simple as providing
the correct scope url for the api. See 'Contributions.'

Contributions
--------------------------------------------------

Contributions are welcome through github pull requests or
issues. Especially for increasing the available scope of services.
