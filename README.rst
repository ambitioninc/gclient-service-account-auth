GClient API Service Account Authorization
=========================================

.. image:: https://travis-ci.org/ambitioninc/gclient-service-account-auth.png
   :target: https://travis-ci.org/ambitioninc/gclient-service-account-auth

.. image:: https://pypip.in/v/gclient-service-account-auth/badge.png
    :target: https://crate.io/packages/gclient-service-account-auth/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/gclient-service-account-auth/badge.png
    :target: https://crate.io/packages/gclient-service-account-auth/
    :alt: Number of PyPI downloads

Authorizing server-to-server communications with Google's APIs should
be easy. However, it can be difficult to understand how to do
authorization based on Google's `Service Accounts`_, instead of the
better-documented three-party oauth flow. This library
attempts to streamline this process.

It makes authentication and authorization as simple as creating an
instance of the `AuthorizedService` class, with the name of your
project and the name of the API to authorize for. To get started, see
the `quickstart`_ guide.

.. _Service Accounts: https://developers.google.com/accounts/docs/OAuth2ServiceAccount

.. _quickstart: http://gclient-service-account-auth.readthedocs.org/en/latest/quickstart.html

Installation
------------
To install the latest release, type::

    pip install gclient-service-account-auth

To install the latest code directly from source, type::

    pip install git+git://github.com/ambitioninc/gclient-service-account-auth.git

Documentation
=============

Full documentation is available at http://gclient-service-account-auth.readthedocs.org

License
=======
MIT License (see LICENSE)

