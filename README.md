# TexBib
Texbib is a program that helps you to manage your BibTeX references.

[![Test status](https://github.com/frcl/texbib/actions/workflows/tests.yml/badge.svg)](https://github.com/frcl/texbib/actions/workflows/tests.yml)
[![PyPI status](https://img.shields.io/pypi/v/texbib?style=flat-square)](https://pypi.org/project/texbib/)

## Installation
I recommend installing texbib using `pipx` or a similar tool with the following command
```
pipx install texbib
```

## Usage

### Basics
To add the contents of a BibTeX `foo.bib` file to the global bibliography type into a shell
```
$ bib add foo.bib
```
You can also pipe BibTeX data via stdin:
```
$ cat paper.bib | bib add -
```
You can specify as many files as you want in a single command.
The entries in the bibliography can be addressed by the ID that is specified in the BibTeX file.

You can also add a reference via its [DOI](https://en.wikipedia.org/wiki/Digital_object_identifier),
either in the `doi:…` format or as URL starting with `https://doi.org/`.
```
$ bib add doi:10.1002/andp.19053220806
```
This will make a request to the crossref API.
ISBNs are also supported:
```
$ bib add 9780123456789
```
Preprints from arXiv may be added similarly:
```
$ bib add arXiv:1306.4856
```
The full-text PDF can be downloaded at the same time (only supported for arXiv at the moment):
```
$ bib add arXiv:1306.4856 --fulltext
```

### Viewing References
Have a look at the references in the bibliography with:
```
$ bib show
```
Sort by ID (`-s i`), author (`-s a`), title (`-s t`), or year (`-s d`):
```
$ bib show -s a
```
Reverse the sort order:
```
$ bib show -s d -r
```
Show details for specific entries:
```
$ bib detail foo2000
$ bib detail foo2000 --format bibtex
```
Search for references matching patterns:
```
$ bib find quantum
$ bib find author title -s d
$ bib find -b myBib "search term"    # search in specific bibliography
```

### Modifying references
Edit an entry in your editor (`$EDITOR` or nano):
```
$ bib edit foo2000
```
Link a local PDF file to an entry:
```
$ bib link-file foo2000 paper.pdf
```
If the reference was added with the `--fulltext` flag it will already have been linked.
Open the PDF associated with an entry:
```
$ bib open foo2000
```

### Using Bibliographies
You can group your references into bibliographies. To create one called `myBib`
```
$ bib init myBib
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
Or renamed:
```
$ bib rename oldName newName
```

### Exporting
Later you probably want to create a new file with all the references in your document directory.
Use the handy `dump` command for that.
```
$ bib dump
```
This will print the full bibliography onto stdout.
Dump to a specific file:
```
$ bib dump myreferences.bib
```

### Removing References
To remove a single item with ID `foo2000` from the active bibliography
```
$ bib rm foo2000
```
