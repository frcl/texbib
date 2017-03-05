"""
Tests for the Bibliography class from the texbib.bibliography module.
"""

import pytest
from texbib import BibItem


REQUIRED = ('ID', 'ENTRYTYPE', 'author', 'year', 'title')

BIBITEM_EXAMPLES = [
    {'SomeLabel': {'ENTRYTYPE' : 'article',
                   'ID'   : 'SomeLabel',
                   'author': 'Max Mustermann',
                   'title': 'Einführung in das Sammeln von Briefmarken',
                   'abstract': ''}}]


# @pytest.mark.parametrize('bibdata', BIBITEM_EXAMPLES)
# def test_repr_is_valid_json(bibdata):
    # assert dict(BibItem(bibdata)) == bibdata
