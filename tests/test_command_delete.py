import pytest


def test_simple_deletion(commands, monkeypatch):
    delete = commands['delete']
    monkeypatch.setattr(commands.run, 'input', lambda: 'y')
    commands.run.activate('foo')
    commands.run.activate('bar')
    delete('foo')
    assert not commands.run.bibdir.joinpath('foo.db').exists()
    assert commands.run.active_name == 'bar'


def test_deleting_active(commands):
    pass # TODO: define behavier


def test_non_existing(commands, capsys):
    delete = commands['delete']
    with pytest.raises(SystemExit):
        delete('123bar')
    _, err = capsys.readouterr()
    assert 'FileNotFound' in err
