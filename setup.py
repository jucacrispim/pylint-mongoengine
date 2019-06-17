# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

DESCRIPTION = 'A Pylint plugin to help it understand MongoEngine'

setup(
    name='pylint-mongoengine',
    url='https://github.com/jucacrispim/pylint-mongoengine',
    author='Juca Crispim',
    author_email='juca@poraodojuca.net',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    version='0.3.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pylint>=2.0', 'pylint-plugin-utils>=0.5'
    ],
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=['pylint', 'mongoengine', 'plugin'],
    zip_safe=False,
)
