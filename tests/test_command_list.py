import pytest


def test_listing(commands, capsys):
    commands['list']()
    out, _ = capsys.readouterr()
    assert 'test0' in out
    assert 'test1' in out
    assert 'default' in out


def test_no_bibs(init_commands, capsys):
    init_commands['list']()
    out, _ = capsys.readouterr()
    assert 'default' in out
    assert not 'activate' in out


def test_file_not_bib(commands, capsys):
    commands.run.bibdir.joinpath('foo.bib').touch()
    commands['list']()
    out, _ = capsys.readouterr()
    assert 'default' in out
    assert not 'activate' in out
