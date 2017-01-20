from setuptools import setup
from texbib import __version__


setup(
    name='texbib',
    version=__version__,
    description='A tool for manageing BibTeX references',
    long_description='',
    url='https://github.com/DrFrankeStein/texbib',
    author='Lars Franke',
    # author_email='pypa-dev@googlegroups.com',

    # TODO: Choose your license
    # license='GPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Text Processing :: Markup :: LaTeX'
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        # TODO: Pick your license as you wish (should match "license" above)
        # 'License :: OSI Approved :: MIT License',
    ],
    keywords='bibtex latex science writing',
    packages=['texbib'], #, 'texbib.parser'],
    install_requires=['bibtexparser'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['pytest'],
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here. If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
        # 'sample': ['package_data.dat'],
    # },
    entry_points={
        'console_scripts': [
            'texbib=texbib:run_texbib',
        ],
    },
)
