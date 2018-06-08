import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='gcp-quota-exporter',
    version='0.1',
    description='GCP Quota Exporter to Prometheus',
    packages=[],
    include_package_data=True,
    long_description=read('README.md'),
    install_requires=[
        'google-api-python-client',
        'oauth2client',
        'prometheus_client',
    ]
)
