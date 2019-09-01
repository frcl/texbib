import pytest


BIBCODE = """@ArTiCle{SomeLabel,
author = {Max Mustermann},
title=  {Einführung in das Sammeln von Briefmarken},
abstract= {},
year = {1999}
}"""


def test_gets_removed(commands):
    label = 'SomeLabel'

    with commands.run.open('w') as bib:
        bib.update(BIBCODE)
        assert label in bib

    commands['rm']([label])

    with commands.run.open() as bib:
        assert label not in bib


def test_unknown_id(commands, capsys):
    with commands.run.open('w') as bib:
        bib.update(BIBCODE)
    commands['rm']('SomeLabel')
    _, err = capsys.readouterr()
    assert 'IdNotFound' in err
