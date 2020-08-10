# coding=utf-8
"""
Setup for scikit-surgery-evaluation
"""

from setuptools import setup, find_packages
import versioneer

# Get the long description
with open('README.rst') as f:
    long_description = f.read()

setup(
    name='scikit-surgery-evaluation',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='A python library for performing surgical skills evaluation',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/UCL/scikit-surgery-evaluation',
    author='Stephen Thompson',
    author_email='YOUR-EMAIL@ucl.ac.uk',
    license='BSD-3 license',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',


        'License :: OSI Approved :: BSD License',


        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',

        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
    ],

    keywords='medical imaging',

    packages=find_packages(
        exclude=[
            'doc',
            'tests',
            'data',
        ]
    ),

    install_requires=[
        'numpy',
        'ipykernel',
        'nbsphinx',
        'vtk',
        'PySide2',
        'scikit-surgeryvtk>=0.12.3',
        'scikit-surgerycore',
        'scikit-surgeryutils',
        'scikit-surgerynditracker',
        'scikit-surgeryarucotracker>=0.0.4'
    ],

    entry_points={
        'console_scripts': [
            'sksurgeryeval=sksurgeryeval.__main__:main',
        ],
    },
)
