import pytest


def test_simple_deletion(commands, monkeypatch):
    monkeypatch.setattr(commands.run, 'input', lambda: 'y')
    commands.run.activate('foo')
    commands.run.activate('bar')
    assert commands.run.is_bib('foo')
    commands['delete']('foo')
    assert not commands.run.is_bib('foo')


def test_deleting_active(commands):
    pass # TODO: define behavier


def test_non_existing(commands, capsys):
    with pytest.raises(SystemExit):
        commands['delete']('123bar')
    _, err = capsys.readouterr()
    assert 'FileNotFound' in err
