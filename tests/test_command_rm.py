import pytest


BIBCODE = """@ArTiCle{SomeLabel,
author = {Max Mustermann},
title=  {Einführung in das Sammeln von Briefmarken},
abstract= {},
year = {1999}
}"""


def test_gets_removed(commands):
    rm = commands['rm']
    label = 'SomeLabel'
    commands.run.active.update(BIBCODE)
    assert label in commands.run.active
    rm([label])
    assert label not in commands.run.active


def test_unknown_id(commands, capsys):
    rm = commands['rm']
    commands.run.active.update(BIBCODE)
    rm('SomeLabel')
    _, err = capsys.readouterr()
    assert 'IdNotFound' in err
