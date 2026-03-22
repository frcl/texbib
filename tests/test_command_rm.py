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


def test_id_not_found_exit_code(commands, monkeypatch):
    from texbib.errors import ExitCode
    import texbib.cli
    import sys

    class ExitCall(Exception):
        pass

    exit_code_called = []
    def foo(c):
        exit_code_called.append(c)
        raise ExitCall
    monkeypatch.setattr(sys, 'exit', foo)


    class MockCommands:
        def set_runtime(self, _):
            pass
        def __call__(self):
            return commands
    monkeypatch.setattr(texbib.cli, 'commands', MockCommands())

    try:
        texbib.cli.main({
            'command': 'rm',
            'objects': ['OtherLabel'],
            'debug': False,
            'config': None
        })
    except ExitCall as e:
        assert exit_code_called[0] == ExitCode.ID_NOT_FOUND
    else:
        assert False