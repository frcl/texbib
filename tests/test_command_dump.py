import os
import pytest


BIBCODE = """@ArTiCle{SomeLabel,
author = {Max Mustermann},
title=  {Einführung in das Sammeln von Briefmarken},
abstract= {},
year = {1999}
}"""


def test_dumped_file_valid(commands):
    dump = commands['dump']
    commands.run.active.update(BIBCODE)
    item = commands.run.active['SomeLabel']
    path = commands.run.texbibdir.joinpath('test.bib')
    dump(str(path))
    with path.open() as bibfile:
        commands.run.active.update(bibfile.read())
    assert item == commands.run.active['SomeLabel']


# def test_non_existing_bib(commands, capsys):
    # dump = commands['dump']
    # commands.run.active.update(BIBCODE)
    # path = commands.run.texbibdir.joinpath('test.bib')
    # dump(str(path))


def test_empty_bib(commands):
    dump = commands['dump']
    path = commands.run.texbibdir.joinpath('test.bib')
    dump(str(path))
    with path.open() as bibfile:
        commands.run.active.update(bibfile.read())


def test_no_filename(commands, tmpdir):
    dump = commands['dump']
    commands.run.activate('test')
    path = tmpdir.join('test.bib')
    os.chdir(tmpdir)
    dump()
    assert path.exists()
