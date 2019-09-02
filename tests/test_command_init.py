import pytest


def test_creation(commands):
    commands['init']('foo')
    assert commands.run.bib_path('foo').exists()


def test_ask_for_overwrite(commands, capsys, monkeypatch):
    commands['init']('bar')

    monkeypatch.setattr(commands.run, 'input', lambda: 'y')
    with commands.run.open('w') as bib:
        bib.update(
            """@book{foo,
                author = "Mr. Mister",
                year = 1999,
                title = "The title"
            }""")
    commands['init']('bar')
    out, _ = capsys.readouterr()
    assert 'Overwrite' in out
    assert commands.run.active_path.exists()


def test_invalid_name(commands, capsys):
    with pytest.raises(SystemExit):
        commands['init']('')
    _, err = capsys.readouterr()
    assert 'InvalidName' in err
