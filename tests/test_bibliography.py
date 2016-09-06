import pytest
from texbib import Bibliography


required = ('ID', 'ENTRYTYPE', 'author', 'year', 'title')

bibcode = """@ArTiCle{SomeLabel,
author = {Max Mustermann},
title=  {Einführung in das Sammeln von Briefmarken},
abstract= {},
year = {1999}
}"""


@pytest.fixture
def bib():
    with Bibliography('TEST', 't') as bb:
        bb.update(bibcode)
        yield bb


@pytest.fixture
def empty_bib():
    with Bibliography('ETEST', 't') as bb:
        yield bb


def test_getitem(bib):
    assert bib['SomeLabel']['author'] == 'Max Mustermann'


def test_getitem_raises_on_unknown_key(bib):
    with pytest.raises(KeyError):
        bib['foo']


def test_database_file_exists(bib):
    assert bib.path.exists()


def test_ids_is_iterator(bib):
    assert hasattr(bib.ids(), '__next__')


def test_ids_stops_iteration(empty_bib):
    with pytest.raises(StopIteration):
        next(empty_bib.ids())


def test_values(bib):
    for item in bib.values():
        for key in required:
            assert key in item


def test_len_update(empty_bib):
    assert len(empty_bib) == 0
    empty_bib.update(bibcode)
    assert len(empty_bib) == 1


def test_seach(bib):
    for item in bib.search('ome'):
        assert item['author'] == 'Max Musterman'
