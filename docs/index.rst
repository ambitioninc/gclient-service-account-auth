GClient Service Account Auth
============================

Authorizing server to server communications with Google's APIs should
be easy. However, it can be difficult to understand how to use
server-to-server authorization, based on Google's `Service Accounts`_,
instead of the better-documented three-party oauth flow. This library
attempts to streamline this process.

It makes authetication and authorization as simple as creating an
instance of the `AuthorizedService` class, with the name of your
project and the name of the API to authorize for. To get started, see
the `quickstart`_ guide.

.. _Service Accounts: https://developers.google.com/accounts/docs/OAuth2ServiceAccount

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   ref/service_account_auth
   contributing
   release_notes
