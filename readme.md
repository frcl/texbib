# TexBib
Texbib is a program that helps you to manage your BibTeX references.

<!-- TODO: installation section -->

## Usage

### Basics
To add the contents of a BibTeX `foo.bib` file to the global bibliography type into a shell
```sh
texbib add foo.bib
```
You can specify as many files as you want in a singe command.
The entries in the bibliography can be adressed by the ID that is spacified in the BibTeX file.
<!--If there was no ID specified the ID are the first four letter of the authors name followed directly by the year of publication.-->

Later you probably want to create a new file with all the references in your document directory.
Use the handy `dump` command for that.
```sh
texbib dump
```

To remove a single item with ID `foo2000` from the global bibliography
```sh
texbib rm foo2000
```

You can find out what references are in the bibliography with
```sh
texbib show all
```


### Using Bibliographies
You can group your references into bibliographies. To create one called `fooBib`
```sh
texbib mkbib fooBib
```

It can be removed with
```sh
texbib rmbib fooBib
```

To add the contents of a file to a biliography use the `addto` command.
```sh
texbib addto fooBib foo.bib
```

<!-- TODO: API section

