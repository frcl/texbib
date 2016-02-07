import os
os.chdir('/home/lars/src/texbib')
from .. import parse
import unittest

class KnownCodeTests(unittest.TestCase):
    bibcode=[ (
    """@ArTiCle{SomeLabel,
        author = {Max Musterman},
        title=  {Einführung in das Sammeln von Briefmarken},
        abstract= {}
        """,
        {   'TYPE' : 'article',
            'ID'   : 'SomeLabel',
            'autor': 'Max Musterman',
            'title': 'Einführung in das Sammeln von Briefmarken',
            'abstract': '' } ) ]

    def testLoadsWithKown(self):
        for bibstring,bibdata in self.bibcode:
            result = parse.loads(bibstring)
            self.assertEqual(result, bibdata)

    def testDumpsWithKnown(self):
        for bibstring,bibdata in self.bibcode:
            result = parse.dumps(bibdata)
            self.assertEqual(result, bibstring)

class LoadsBadInputTests(unittest.TestCase):
    def testEmpty(self):
        self.assertRaises(ValueError, parse.loads, '@{title={},author={}}')
        self.assertRaises(ValueError, parse.loads, '@ARTICLE{}')

    def testIncomplete(self):
        incompleteCode="@ARTICLE{label,title={},author={},"
        self.assertRaises(ValueError, parse.loads, incompleteCode)
        incompleteCode="@ARTICLE{label,title={,author={}}"
        self.assertRaises(ValueError, parse.loads, incompleteCode)

    #TODO: make more tests
    #       * missing '='
    #       * unknown Type
    #       * wrong commas

class DumpsBadInputTests(unittest.TestCase):
    bibitem = { 
        'ID'   : 'SomeLabel',
        'TYPE' : 'article', 
        'autor': 'Max Musterman',
        'title': 'Einführung in das Sammeln von Briefmarken',
        'abstract': '' }

    def testNoType(self):
        noType=bibitem
        noType['TYPE']=''
        self.assertRaises(ValueError, parse.dumps, noType)
        del noType['TYPE']
        self.assertRaises(ValueError, parse.dumps, noType)

