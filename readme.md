# Bib
Texbib is a program that helps you to manage your BibTeX references.

[![Build Status](https://travis-ci.org/frcl/texbib.svg?branch=master)](https://travis-ci.org/frcl/texbib)

## Installation
To install bib use the following commands

```
git clone https://github.com/frcl/texbib
cd texbib
pip install .
```

Since bib is not stable right now, consider installing it in a virtualenv or locally with the `--user` flag.

## Usage

### Basics
To add the contents of a BibTeX `foo.bib` file to the global bibliography type into a shell
```
$ bib add foo.bib
```
You can specify as many files as you want in a singe command.
The entries in the bibliography can be addressed by the ID that is specified in the BibTeX file.

Later you probably want to create a new file with all the references in your document directory.
Use the handy `dump` command for that.
```
$ bib dump
```

To remove a single item with ID `foo2000` from the global bibliography
```
$ bib rm foo2000
```

You can find out what references are in the bibliography with
```
$ xbib show
```


### Using Bibliographies
You can group your references into bibliographies. To create one called `fooBib`
```
bib create fooBib
```
After creation it is your new active bibliography.
Everything you add and remove will be appliyed to it instead of the default one.

To see what bibliographies exist and which is active
```
$ bib list
```

To change the active bibliography to an existing one use the `open` command.
```
$ bib open fooBib
```

A bibliography can be removed with
```
$ bib delete fooBib
```

<!-- TODO: API section -->
