#!/usr/bin/env python2
from setuptools import setup, find_packages
from codecs import open
from os import path

readme = 'A wrapper for the new Tobii Pro SDK based on Psychopy'
if path.isfile('README.md'):
    readme = open('README.md', 'r').read()

setup(
    name='tobii_pro_wrapper',
    version= '0.1.0',
    description='A wrapper for the new Tobii Pro SDK based on Psychopy.',
    long_description=  readme,
    url='https://github.com/oguayasa/tobii_pro_wrapper',
    download_url='https://github.com/oguayasa/tobii_pro_wrapper',
    # Author details
    author='Olivia Guayasamin',
    author_email='oguayasa@gmail.com',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Code Generators',
        'License :: OSI Approved :: Apache Software License',
        # Only the following because these work w/ psychopy
        'Programming Language :: Python :: 2.7',
    ],
    keywords=['tobii', 'eyetracking', 'gazetracking'],
    packages=['tobii_pro_wrapper'],
    install_requires=['numpy', 'scipy', 'psychopy', 'datetime', 'random',
                      'collections', 'win32api', 'tobii_research'],
    # package_data={
    #     '': ['templates/*.tpl']
    # },
)
