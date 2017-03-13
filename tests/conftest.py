import pytest

from texbib.runtime import RuntimeInstance
from texbib.commands import commands as _commands


@pytest.fixture(scope="module")
def runtime(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('test')
    run = RuntimeInstance('fake', fakedir=tmpdir)
    run.activate('test')
    return run


@pytest.fixture(scope="module")
def init_runtime(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('init')
    run = RuntimeInstance('fake', fakedir=tmpdir)
    return run


@pytest.fixture(scope="module")
def commands(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('com')
    run = RuntimeInstance('fake', fakedir=tmpdir)
    _commands.set_runtime(run)
    _commands.run.activate('test1')
    _commands.run.activate('test0')
    return _commands()


@pytest.fixture(scope="module")
def init_commands(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('com')
    run = RuntimeInstance('fake', fakedir=tmpdir)
    _commands.set_runtime(run)
    return _commands()
