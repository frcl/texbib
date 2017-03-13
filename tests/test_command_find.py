import pytest


BIBCODE = """@ArTiCle{SomeLabel,
author = {Max Mustermann},
title=  {Einführung in das Sammeln von Briefmarken},
abstract= {},
year = {1999}
}"""


@pytest.mark.xfail
def test_simple_gets_found(commands, capsys):
    find = commands['find']
    commands.run.active.update(BIBCODE)
    find('mustermann')
    out, _ = capsys.readouterr()
    assert "SomeLabel" in out
    find('term')
    out, _ = capsys.readouterr()
    assert "SomeLabel" in out


def test_unmatched_finds_nothing(commands, capsys):
    find = commands['find']
    commands.run.active.update(BIBCODE)
    find('foobar23')
    out, _ = capsys.readouterr()
    assert out.strip() == ''


@pytest.mark.xfail
def test_more_than_one_searchterm(commands, capsys):
    find = commands['find']
    commands.run.active.update(BIBCODE)
    find('max', 'man')
    out, _ = capsys.readouterr()
    assert "SomeLabel" in out
