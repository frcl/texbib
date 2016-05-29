from texbib.bibliography import Bibliography

def test_ids():
    with Bibliography('TEST') as bib:
        assert hasattr(bib.ids(),'__next__')
