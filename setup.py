"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

import motey


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        import pytest, sys
        sys.exit(pytest.main(self.test_args))


setup(
    name = motey.__appname__,
    version = motey.__version__,
    description = 'A fog node prototype.',
    long_description = long_description,
    url = motey.__url__,
    author = motey.__author__,
    author_email = motey.__email__,
    license = motey.__licence__,
    classifiers = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Utilities',
        'Topic :: Internet of Things',
        'License :: Apache Version 2.0',
        'Natural Language :: English',
        'Operating System :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords = ['cli', 'IoT', 'Fog Node'],
    packages = find_packages(exclude=['docker-image', 'docs', 'resources', 'samples', 'scripts', 'tests*', 'webclient']),
    include_package_data=True,
    zip_safe=False,
    install_requires = [
        'aiofiles==0.3.1',
        'click==6.7',
        'daemonize==2.4.7',
        'docker==2.2.1',
        'docker-pycreds==0.2.1',
        'docopt==0.6.2',
        'docutils==0.13.1',
        'Flask==0.12.1',
        'future==0.16.0',
        'gevent==1.2.1',
        'greenlet==0.4.12',
        'httptools==0.0.9',
        'itsdangerous==0.24',
        'Jinja2==2.9.6',
        'jsonschema==2.6.0',
        'lockfile==0.12.2',
        'Logbook==1.0.0',
        'MarkupSafe==1.0',
        'msgpack-python==0.4.8',
        'paho-mqtt==1.2.3',
        'psutil==5.2.2',
        'PyYAML==3.12',
        'pyzmq==16.0.2',
        'requests==2.13.0',
        'Rx==1.5.9',
        'sanic==0.5.2',
        'six==1.10.0',
        'tinydb==3.2.3',
        'typing==3.6.1',
        'ujson==1.35',
        'uvloop==0.8.0',
        'websocket-client==0.40.0',
        'websockets==3.3',
        'Werkzeug==0.12.1',
        'Yapsy==1.11.223',
        'zerorpc==0.6.1',
    ],
    tests_require = {
        'pycodestyle==2.3.1',
        'pytest',
        'mock',
    },
    entry_points = {
        'console_scripts': [
            'motey = motey.cli.main:main',
        ],
    },
    cmdclass = {'test': RunTests},
)
