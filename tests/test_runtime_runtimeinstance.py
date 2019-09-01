import pytest


from texbib.utils import Events, Levels


def test_init_state(init_runtime):
    assert {path.name for path in init_runtime.bibdir.iterdir()} \
            == {'default', 'ACTIVE'}
    init_runtime.activate('test')
    assert (init_runtime.bibdir/'test'/'metadata.db').exists()


def test_paths(runtime):
    assert runtime.bibdir.is_dir()
    assert runtime.state_path.name == 'ACTIVE'


def test_activate(runtime):
    assert runtime.active_name == 'test'
    runtime.activate('default')
    assert runtime.active_name == 'default'
    runtime.activate('new_bib')
    assert runtime.active_name == 'new_bib'
    with pytest.raises(ValueError):
        runtime.activate('')


def test_event(runtime, capsys):
    runtime.event(Events.FileNotFound, 'filename.foo', Levels.warning, None)
    _, err = capsys.readouterr()
    assert 'bib' in err
    assert 'FileNotFound' in err


def test_ask(runtime, capsys, monkeypatch):
    monkeypatch.setattr(runtime, 'input', lambda: 'y')
    answer = runtime.ask('FOO?')
    assert 'FOO?' in capsys.readouterr()[0]
    assert answer
    monkeypatch.setattr(runtime, 'input', lambda: '')
    answer = runtime.ask('FOO?', default=False)
    out, _ = capsys.readouterr()
    assert 'FOO?' in out
    assert '(y/N)' in out
    assert not answer
