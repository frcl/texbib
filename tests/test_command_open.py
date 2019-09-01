import json


def test_existing(commands):
    testbib = 'test1'
    commands['checkout'](testbib)
    assert commands.run.active_name == testbib
    assert commands.run.active_path.exists()
    with commands.run.state_path.open() as statefile:
        assert json.load(statefile)['bib'] == testbib


def test_non_existing(commands, monkeypatch):
    testbib = 'nobib'
    monkeypatch.setattr(commands.run, 'input', lambda: 'n')
    commands['checkout'](testbib)
    assert not commands.run.bib_path(testbib).exists()
    monkeypatch.setattr(commands.run, 'input', lambda: 'y')
    commands['checkout'](testbib)
    assert commands.run.bib_path(testbib).exists()


def test_already_active(commands, capsys):
    testbib = 'test0'
    commands['checkout'](testbib)
    assert commands.run.active_name == testbib
    commands['checkout'](testbib)
    assert commands.run.active_name == testbib
    with commands.run.state_path.open() as statefile:
        assert json.load(statefile)['bib'] == testbib
    out, _ = capsys.readouterr()
    assert 'Already using' in out
