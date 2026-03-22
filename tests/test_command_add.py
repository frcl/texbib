import sys


def test_adding_file(commands, tmpdir):
    path = tmpdir.join('test.bib')
    with path.open('w') as testfile:
        testfile.write("""@book{foo,
            author = "Mr. Mister",
            year = 1999,
            title = "The title"
        }""")
    commands['add']([str(path)])
    with commands.run.open() as bib:
        assert 'foo' in bib.db.keys()


def test_skip_non_existing(commands, tmpdir, capsys):
    commands['add']([str(tmpdir.join('foo.bib'))])
    _, err = capsys.readouterr()
    assert 'File not found' in err


def test_empty_list(commands):
    commands['add']([])


def test_adding_from_stdin(commands, tmpdir, monkeypatch, capsys):
    monkeypatch.setattr(
        sys, 'stdin',
        type('StdinMock', (), {'read': lambda self: 
            '@book{test_stdin,\n'
            '    author = "Test Author",\n'
            '    year = 2024,\n'
            '    title = "Stdin Test"\n'
            '}'})())
    commands['add'](['-'])
    with commands.run.open() as bib:
        assert 'test_stdin' in bib.db.keys()
    out, _ = capsys.readouterr()
    assert 'test_stdin' in out


def test_adding_empty_stdin(commands, capsys, monkeypatch):
    monkeypatch.setattr(
        sys, 'stdin',
        type('StdinMock', (), {'read': lambda self: ''})())
    from texbib.errors import ExitCode
    result = commands['add'](['-'])
    _, err = capsys.readouterr()
    assert 'no data from stdin' in err
    assert result != ExitCode.SUCCESS
