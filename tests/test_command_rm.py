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
    commands['rm'](['OtherLabel'])
    _, err = capsys.readouterr()
    assert 'Reference' in err
    assert 'not found' in err
