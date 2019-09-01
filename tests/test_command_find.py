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
    with commands.run.open('w') as bib:
        bib.update(BIBCODE)
    find('mustermann')
    out, _ = capsys.readouterr()
    assert 'SomeLabel' in out
    find('term')
    out, _ = capsys.readouterr()
    assert 'SomeLabel' in out


def test_unmatched_finds_nothing(commands, capsys):
    with commands.run.open('w') as bib:
        bib.update(BIBCODE)
    commands['find']('foobar23')
    out, _ = capsys.readouterr()
    assert out.strip() == ''


@pytest.mark.xfail
def test_more_than_one_searchterm(commands, capsys):
    with commands.run.open('w') as bib:
        bib.update(BIBCODE)
    commands['find']('max', 'man')
    out, _ = capsys.readouterr()
    assert 'SomeLabel' in out
