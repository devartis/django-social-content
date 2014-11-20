#!/usr/bin/env python

from setuptools import setup, find_packages
from devartis_admin import VERSION

github_url = 'https://github.com/devartis/django-social-content'
long_desc = '''
%s

%s
''' % (open('README').read(), open('CHANGELOG').read())

setup(
    name='django-social-admin',
    version=VERSION.replace(' ', '-'),
    description='Downloads feeds from Twitter, Facebook and Youtube',
    long_description=long_desc,
    author='Pablo García',
    author_email='poli@devartis.com',
    url=github_url,
    download_url='%s/archive/%s.tar.gz' % (github_url, VERSION),
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False,
)