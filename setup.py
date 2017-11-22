# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
exec(open('nanogui/version.py').read())

setup(
    name='NanoGUI',
    version=__version__,
    description='GUI for NanoPlot',
    long_description=open(path.join(here, "README.rst")).read(),
    url='https://github.com/wdecoster/nanogui',
    author='Wouter De Coster',
    author_email='decosterwouter@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='nanopore sequencing plotting quality control',
    packages=find_packages(),
    install_requires=['nanoplotter>=0.25.0',
                      'nanoget>=1.0.2',
                      'nanomath>=0.14.2',
                      'NanoPlot>=1.3.3'
                      ],
    package_data={'NanoGUI': []},
    package_dir={'nanogui': 'nanogui'},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'NanoGUI=nanogui.nanogui:main',
        ],
    },
)
