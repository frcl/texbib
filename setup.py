from setuptools import setup
import re


def version():
    with open('texbib/__init__.py', 'r') as init_file:
        _version = re.search('__version__ = \'([^\']+)\'',
                             init_file.read()).group(1)
    return _version


def readme():
    with open('readme.rst', 'r') as readme_file:
        _readme = readme_file.read()
    return _readme


setup(
    name='texbib',
    version=version(),
    description='A tool for manageing BibTeX references',
    long_description=readme(),
    url='https://github.com/frcl/texbib',
    author='Lars Franke',
    author_email='lars.franke@mailbox.org',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Text Processing :: Markup :: LaTeX',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    keywords='bibtex latex science writing',
    packages=['texbib'],
    install_requires=['bibtexparser'],
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'texbib=texbib.cli:cli',
        ],
    },
)
