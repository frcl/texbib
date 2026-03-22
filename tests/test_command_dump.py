import os
import pytest


BIBCODE = """@ArTiCle{SomeLabel,
author = {Max Mustermann},
title=  {Einführung in das Sammeln von Briefmarken},
abstract= {},
year = {1999}
}"""


def test_dumped_file_valid(commands, tmpdir):
    with commands.run.open('w') as bib:
        bib.update(BIBCODE)
        item = bib['SomeLabel']
    path = tmpdir.join('test.bib')
    commands['dump'](str(path))
    with path.open() as bibfile, \
         commands.run.open('w') as bib:
        bib.update(bibfile.read())
        assert item == bib['SomeLabel']


# def test_non_existing_bib(commands, capsys):
    # dump = commands['dump']
    # commands.run.active.update(BIBCODE)
    # path = commands.run.bibdir.joinpath('test.bib')
    # dump(str(path))


def test_empty_bib(init_commands, tmpdir):
    path = tmpdir.join('empty.bib')
    init_commands['dump'](str(path))
    with path.open() as bibfile, \
         init_commands.run.open('w') as bib:
        text = bibfile.read()
        assert not text.strip()
        bib.update(text)


def test_no_filename(commands, capsys):
    with commands.run.open('w') as bib:
        bib.update(BIBCODE)
    commands['dump']()
    out, _ = capsys.readouterr()
    assert 'author = {Max Mustermann}' in out
