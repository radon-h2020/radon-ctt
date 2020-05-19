# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "openapi_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.0.2",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0",
    'flask',
    'sqlalchemy',
    'marshmallow'
]

setup(
    name=NAME,
    version=VERSION,
    description="RADON CTT Server API",
    author_email="",
    url="",
    keywords=["OpenAPI", "RADON CTT Server API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['openapi_server=openapi_server.__main__:main']},
    long_description="""\
    This is API of the RADON Continuous Testing Tool (CTT) Server: &lt;a href&#x3D;\&quot;https://github.com/radon-h2020/radon-ctt\&quot;&gt;https://github.com/radon-h2020/radon-ctt&lt;a/&gt;
    """
)

