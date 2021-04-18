# Bib
Texbib is a program that helps you to manage your BibTeX references.

[![Build Status](https://travis-ci.org/frcl/texbib.svg?branch=master)](https://travis-ci.org/frcl/texbib)

## Installation
To install bib use the following commands

```
pip install --user texbib
```

## Usage

### Basics
To add the contents of a BibTeX `foo.bib` file to the global bibliography type into a shell
```
$ bib add foo.bib
```
You can specify as many files as you want in a singe command.
The entries in the bibliography can be addressed by the ID that is specified in the BibTeX file.

You can also add a reference via its [DOI](https://en.wikipedia.org/wiki/Digital_object_identifier),
either in the `doi:…` format or as URL starting with `https://doi.org/`.
```
$ bib add doi:10.1002/andp.19053220806
```
This will make a request to the crossref api.

Preprints from arXiv may be added similarly:
```
$ bib add arXiv:1306.4856
```
You can have a look at the references in the bibliography with
```
$ bib show
```
Later you probably want to create a new file with all the references in your document directory.
Use the handy `dump` command for that.
```
$ bib dump
Wrote to default.bib
```
To remove a single item with ID `foo2000` from the active bibliography
```
$ bib rm foo2000
```

### Using Bibliographies
You can group your references into bibliographies. To create one called `myBib`
```
bib init myBib
```
After creation it is your new active bibliography.
Everything you add and remove will be applied to it instead of the default one.

To see what bibliographies exist and which is active
```
$ bib list
  default
* myBib
```
To change the active bibliography to an existing one use the `checkout` command.
```
$ bib checkout default
```
A bibliography can be removed with
```
$ bib delete myBib
```
