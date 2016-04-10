import os as os
import importlib.util


def import_from_dir(dir_local):
    """Imorts bibtexparser functions from a dir

    import_from_dir(BIBTEXPARSERDIR) -> (loads, dumps, BibDatabase)
    """
    spec = importlib.util.spec_from_file_location(
        'bibtexparser',
        os.path.join(dir_local, '__init__.py'))
    btparser = importlib.util.module_from_spec(_spec)
    spec.loader.exec_module(btparser)
    return (btparser.loads,
            btparser.dumps,
            btparser.bibdatabase.BibDatabase)

