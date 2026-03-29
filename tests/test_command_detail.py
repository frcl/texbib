import pytest


BIBCODE = """@book{somekey,
author = {John Smith},
title = {The Book Title},
year = {2020},
journal = {Test Journal},
publisher = {Test Publisher}
}"""


def test_detail_simple_format(commands, capsys):
    detail = commands['detail']
    with commands.run.open('w') as bib:
        bib.update(BIBCODE)
    detail(['somekey'])
    out, _ = capsys.readouterr()
    assert 'somekey' in out
    assert 'Test Journal' in out


def test_detail_bibtex_format(commands, capsys):
    detail = commands['detail']
    with commands.run.open('w') as bib:
        bib.update(BIBCODE)
    detail(['somekey'], format='bibtex')
    out, _ = capsys.readouterr()
    assert '@book{somekey' in out
    assert 'title = {The Book Title}' in out


def test_detail_multiple_ids(commands, capsys):
    detail = commands['detail']
    bibcode = """@book{key1,
author = {Author One},
title = {First Title},
year = {2020}
}
@book{key2,
author = {Author Two},
title = {Second Title},
year = {2021}
}"""
    with commands.run.open('w') as bib:
        bib.update(bibcode)
    detail(['key1', 'key2'])
    out, _ = capsys.readouterr()
    assert 'key1' in out
    assert 'Author One' in out
    assert 'key2' in out
    assert 'Author Two' in out


def test_detail_unknown_id(commands, capsys):
    detail = commands['detail']
    with commands.run.open('w') as bib:
        bib.update(BIBCODE)
    result = detail(['nonexistent'])
    out, err = capsys.readouterr()
    assert "Reference 'nonexistent' not found" in err
    assert result == 5  # ID_NOT_FOUND exit code


def test_detail_unknown_id_with_valid(commands, capsys):
    detail = commands['detail']
    with commands.run.open('w') as bib:
        bib.update(BIBCODE)
    result = detail(['somekey', 'nonexistent'])
    out, err = capsys.readouterr()
    # Valid entry should still be shown
    assert 'somekey' in out
    assert 'John Smith' in out
    # Error for missing entry
    assert "Reference 'nonexistent' not found" in err
    assert result == 5  # ID_NOT_FOUND exit code
