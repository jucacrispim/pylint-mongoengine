# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

LONG_DESCRIPTION = open('README.md').read()

setup(
    name='pylint-mongoengine',
    url='https://github.com/jucacrispim/pylint-mongoengine',
    author='Juca Crispim',
    author_email='juca@poraodojuca.net',
    description='A Pylint plugin to help it understand MongoEngine',
    long_description=LONG_DESCRIPTION,
    version='0.2.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pylint>=2.0', 'pylint-plugin-utils==0.4'
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
