from setuptools import setup
import re


def version():
    with open('texbib/__init__.py', 'r') as init_file:
        _version = re.search('__version__ = \'([^\']+)\'',
                             init_file.read()).group(1)
    return _version


def readme():
    with open('README.md', 'r') as readme_file:
        _readme = readme_file.read()
    return _readme


setup(
    name='texbib',
    version=version(),
    description='A tool for managing bibliographies',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/frcl/bib',
    author='Lars Franke',
    author_email='frcl@mailbox.org',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    keywords='bibtex latex science writing',
    packages=['texbib', 'texbib.sources'],
    install_requires=[
        'bibtexparser',
        'requests',
        'isbnlib',
        'beautifulsoup4',
    ],
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'bib=texbib.cli:cli',
        ],
    },
)
