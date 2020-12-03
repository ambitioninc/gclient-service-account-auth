# import multiprocessing to avoid this bug (http://bugs.python.org/issue15881#msg170215)
import multiprocessing
assert multiprocessing
import re
from setuptools import setup, find_packages


def get_version():
    """
    Extracts the version number from the version.py file.
    """
    VERSION_FILE = 'service_account_auth/version.py'
    mo = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', open(VERSION_FILE, 'rt').read(), re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError('Unable to find version string in {0}.'.format(VERSION_FILE))


setup(
    name='gclient-service-account-auth',
    version=get_version(),
    description=(
        "Easily create an authorized service-object "
        "for interacting with google's client APIs, server to server."
    ),
    long_description=open('README.rst').read(),
    url='http://github.com/ambitioninc/gclient-service-account-auth',
    author='Erik Swanson',
    author_email='TheErikSwanson@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    install_requires=[
        'httplib2>=0.9',
        'google-api-python-client~=1.4',
        'pyopenssl>=0.14',
    ],
    tests_require=[
        'nose',
        'mock',
    ],
    test_suite='nose.collector',
    include_package_data=True,
)
