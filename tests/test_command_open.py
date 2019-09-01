import json


def test_existing(commands):
    testbib = 'test1'
    commands['open'](testbib)
    assert commands.run.active_name == testbib
    assert commands.run.active.path.exists()
    with open(commands.run.bibdir.joinpath('active')) as statefile:
        assert json.load(statefile)['bib'] == testbib


def test_non_existing(commands, monkeypatch):
    testbib = 'nobib'
    monkeypatch.setattr(commands.run, 'input', lambda: 'n')
    commands['open'](testbib)
    assert not commands.run.bibdir.joinpath(testbib + '.db').exists()
    monkeypatch.setattr(commands.run, 'input', lambda: 'y')
    commands['open'](testbib)
    assert commands.run.active.path.exists()


def test_already_active(commands, capsys):
    testbib = 'test0'
    commands['open'](testbib)
    assert commands.run.active_name == testbib
    commands['open'](testbib)
    assert commands.run.active_name == testbib
    with commands.run.bibdir.joinpath('active').open() as statefile:
        assert json.load(statefile)['bib'] == testbib
    _, err = capsys.readouterr()
    assert 'already active' in err


# def test_no_statefile(init_commands.run):
    # testbib = 'test1'
    # commands['open'](testbib)
    # assert init_commands.run.active_name == testbib
    # assert init_commands.run.active.path.exists()
    # assert init_commands.run.bibdir.joinpath('active').exists()
    # with open(init_commands.run.bibdir.joinpath('active')) as statefile:
        # assert json.load(statefile)['bib'] == testbib
