import pytest
import re


BIBCODE = """@ArTiCle{SomeLabel,
author = {Max Mustermann},
title=  {Einführung in das Sammeln von Briefmarken},
abstract= {},
year = {1999}
}"""

BIBCODE_SORT = """@book{aaa2020,
author = {Alice Author},
title = {Alpha Document},
year = {2020}
}
@book{bbb2019,
author = {Bob Builder},
title = {Beta Book},
year = {2019}
}
@book{ccc2021,
author = {Charlie Chef},
title = {Gamma Guide},
year = {2021}
}"""


def _get_ids_from_output(output):
    """Extract bibitem IDs from formatted output."""
    matches = [re.match(r'^\x1b\[95m([A-Za-z0-9_]*)\x1b\[0m$', line) for line in output.split('\n')]
    return [m.groups(0)[0] for m in matches if m]


def test_simple_gets_found(commands, capsys):
    find = commands['find']
    with commands.run.open('w') as bib:
        bib.update(BIBCODE)
    find(['mustermann'])
    out, _ = capsys.readouterr()
    assert 'SomeLabel' in out
    find(['term'])
    out, _ = capsys.readouterr()
    assert 'SomeLabel' in out


def test_unmatched_finds_nothing(commands, capsys):
    with commands.run.open('w') as bib:
        bib.update(BIBCODE)
    commands['find'](['foobar23'])
    out, _ = capsys.readouterr()
    assert out.strip() == ''


def test_smart_case(commands, capsys):
    find = commands['find']
    with commands.run.open('w') as bib:
        bib.update(BIBCODE)
    find(['Mustermann'])
    out, _ = capsys.readouterr()
    assert 'SomeLabel' in out
    find(['MusterMann'])
    out, _ = capsys.readouterr()
    assert out.strip() == ''


def test_more_than_one_searchterm(commands, capsys):
    with commands.run.open('w') as bib:
        bib.update(BIBCODE)
    commands['find'](['max', 'man'])
    out, _ = capsys.readouterr()
    assert 'SomeLabel' in out


def test_sort_by_id(commands, capsys):
    find = commands['find']
    with commands.run.open('w') as bib:
        bib.update(BIBCODE_SORT)
    find([], sort_by='i')
    out, _ = capsys.readouterr()
    ids = _get_ids_from_output(out)
    assert ids == ['aaa2020', 'bbb2019', 'ccc2021']


def test_sort_by_id_reverse(commands, capsys):
    find = commands['find']
    with commands.run.open('w') as bib:
        bib.update(BIBCODE_SORT)
    find([], sort_by='i', reverse=True)
    out, _ = capsys.readouterr()
    ids = _get_ids_from_output(out)
    assert ids == ['ccc2021', 'bbb2019', 'aaa2020']


def test_sort_by_author(commands, capsys):
    find = commands['find']
    with commands.run.open('w') as bib:
        bib.update(BIBCODE_SORT)
    find([], sort_by='a')
    out, _ = capsys.readouterr()
    ids = _get_ids_from_output(out)
    assert ids == ['aaa2020', 'bbb2019', 'ccc2021']


def test_sort_by_author_reverse(commands, capsys):
    find = commands['find']
    with commands.run.open('w') as bib:
        bib.update(BIBCODE_SORT)
    find([], sort_by='a', reverse=True)
    out, _ = capsys.readouterr()
    ids = _get_ids_from_output(out)
    assert ids == ['ccc2021', 'bbb2019', 'aaa2020']


def test_sort_by_title(commands, capsys):
    find = commands['find']
    with commands.run.open('w') as bib:
        bib.update(BIBCODE_SORT)
    find([], sort_by='t')
    out, _ = capsys.readouterr()
    ids = _get_ids_from_output(out)
    assert ids == ['aaa2020', 'bbb2019', 'ccc2021']


def test_sort_by_date(commands, capsys):
    find = commands['find']
    with commands.run.open('w') as bib:
        bib.update(BIBCODE_SORT)
    find([], sort_by='d')
    out, _ = capsys.readouterr()
    ids = _get_ids_from_output(out)
    assert ids == ['bbb2019', 'aaa2020', 'ccc2021']


def test_sort_by_date_reverse(commands, capsys):
    find = commands['find']
    with commands.run.open('w') as bib:
        bib.update(BIBCODE_SORT)
    find([], sort_by='d', reverse=True)
    out, _ = capsys.readouterr()
    ids = _get_ids_from_output(out)
    assert ids == ['ccc2021', 'aaa2020', 'bbb2019']


def test_sort_missing_author_last(commands, capsys):
    find = commands['find']
    bibcode = """@book{noauthor,
title = {No Author Book},
year = {2020}
}
@book{zzaa,
author = {Author A},
title = {Author A Book},
year = {2019}
}"""
    with commands.run.open('w') as bib:
        bib.update(bibcode)
    find([], sort_by='a')
    out, _ = capsys.readouterr()
    ids = _get_ids_from_output(out)
    # Empty author sorts before non-empty (ascending order)
    assert ids == ['noauthor', 'zzaa']


def test_sort_missing_year_last(commands, capsys):
    find = commands['find']
    bibcode = """@book{noyear,
author = {No Year},
title = {No Year Book},
year = {}
}
@book{year2020,
author = {Year 2020},
title = {Year 2020 Book},
year = {2020}
}"""
    with commands.run.open('w') as bib:
        bib.update(bibcode)
    find([], sort_by='d')
    out, _ = capsys.readouterr()
    ids = _get_ids_from_output(out)
    assert ids == ['year2020', 'noyear']


def test_show_with_sort(commands, capsys):
    show = commands['show']
    with commands.run.open('w') as bib:
        bib.update(BIBCODE_SORT)
    show(sort_by='i')
    out, _ = capsys.readouterr()
    ids = _get_ids_from_output(out)
    assert ids == ['aaa2020', 'bbb2019', 'ccc2021']


def test_sort_with_search_pattern(commands, capsys):
    find = commands['find']
    with commands.run.open('w') as bib:
        bib.update(BIBCODE_SORT)
    find(['book'], sort_by='d')
    out, _ = capsys.readouterr()
    ids = _get_ids_from_output(out)
    assert ids == ['bbb2019', 'aaa2020', 'ccc2021']
