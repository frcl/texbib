import pytest


BIBCODE = """@ArTiCle{SomeLabel,
author = {Max Mustermann},
title=  {Einführung in das Sammeln von Briefmarken},
abstract= {},
year = {1999}
}"""


def test_output(commands, capsys):
    show = commands['show']
    commands.run.active.update(BIBCODE)
    show()
    out, _ = capsys.readouterr()
    assert "SomeLabel" in out
    bib = commands.run.active_name
    commands.run.activate('FooBar')
    show(bib)
    assert "SomeLabel" in out


# @pytest.mark.xfail
# def test_short_format(commands, capsys):
    # show = commands['show']


# @pytest.mark.xfail
# def test_long_format(commands, capsys):
    # show = commands['show']


@pytest.mark.xfail
def test_non_existing_bib(commands, capsys):
    show = commands['show']
    show('F00Bar')
    _, err = capsys.readouterr()
    assert 'FileNotFound' in err
