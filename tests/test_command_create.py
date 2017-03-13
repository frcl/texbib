import pytest


def test_creation(commands):
    create = commands['create']
    create('foo')
    assert commands.run.texbibdir.joinpath('foo.db').exists()


def test_ask_for_overwrite(commands, capsys, monkeypatch):
    create = commands['create']
    monkeypatch.setattr(commands.run, 'input', lambda: 'y')
    create('bar')
    commands.run.active.update(
        """@book{foo,
            author = "Mr. Mister",
            year = 1999,
            title = "The title"
        }""")
    create('bar')
    out, _ = capsys.readouterr()
    assert 'Overwrite?' in out
    assert commands.run.active


def test_invalid_name(commands, capsys):
    create = commands['create']
    with pytest.raises(SystemExit):
        create('')
    _, err = capsys.readouterr()
    assert 'InvalidName' in err
