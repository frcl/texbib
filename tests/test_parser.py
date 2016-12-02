"""
Tests for the parserfuntions `loads` and `dumps` from the texbib.parser module.
"""

import pytest
from texbib import parser


BIBCODE_EXAMPLES = [(
    """@ArTiCle{SomeLabel,
    author = {Max Mustermann},
    title=  {Einführung in das Sammeln von Briefmarken},
    abstract= {}
    """,
    {'SomeLabel': {'ENTRYTYPE' : 'article',
                   'ID'   : 'SomeLabel',
                   'author': 'Max Mustermann',
                   'title': 'Einführung in das Sammeln von Briefmarken',
                   'abstract': ''}})]

# loads
# =====

@pytest.mark.parametrize('bibcode,bibdata', BIBCODE_EXAMPLES)
def test_loads_with_known_values(bibcode, bibdata):
    assert parser.loads(bibcode) == bibdata

@pytest.mark.parametrize('bibdata', dict(BIBCODE_EXAMPLES).values())
def test_selfconsistency(bibdata):
    assert parser.loads(parser.dumps(bibdata)) == bibdata


#def test_exception_on_empty_attributes():
#    with pytest.raises(ValueError):
#        parser.loads('@{title={},author={}}')
#    with pytest.raises(ValueError):
#        parser.loads('@ARTICLE{}')


#def test_exception_on_incomplete_record():
#    with pytest.raises(ValueError):
#        parser.loads('@ARTICLE{label,title={},author={},')
#    with pytest.raises(ValueError):
#        parser.loads('@ARTICLE{label,title={,author={}}')

# TODO: make more tests
#       - missing '='
#       - unknown Type
#       - wrong commas


# dumps
# =====

#def test_exception_on_missing_type():
#    noType = BIBCODE_EXAMPLES[0][1]
#
#    del noType['SomeLabel']['TYPE']
#    with pytest.raises(ValueError):
#        parser.dumps(noType)
#
#    noType['SomeLabel']['TYPE'] = ''
#    with pytest.raises(ValueError):
#        parser.dumps(noType)

# TODO: make more tests
