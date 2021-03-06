#!/usr/bin/env python

from setuptools import setup, find_packages
from social_content import VERSION

github_url = 'https://github.com/devartis/django-social-content'
long_desc = '''
%s

%s
''' % (open('README.md').read(), open('CHANGELOG').read())

setup(
    name='django-social-content',
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
    install_requires=[
        "isodate==0.5.4",
    ],
    zip_safe=False,
)
