import re
import shelve
import textwrap
from pathlib import Path
from typing import List, Literal, Optional, Union

from .parser import loads, dumps
from .colors import ColoredText as _c, highlight
from .term_utils import indented, tex2term


def _smart_case(patterns: List[str]) -> bool:
    """Return True if patterns should match case-insensitively.

    Smart case: if any pattern contains uppercase, use case-sensitive matching.
    Otherwise, use case-insensitive matching.
    """
    return not any(re.search(r'[A-Z]', p) for p in patterns)


class BibItem(dict):
    """A dictionary like class that contains data about a single reference.
    A bibitem should always have an ID, author, year and title.
    There can be an arbitrary number other entries.
    """

    def __init__(self, item):
        dict.__init__(self)

        if isinstance(item, dict):
            self.update(item)
        else:
            raise TypeError

    def format_term(self, has_file: bool = False,
                    patterns: Optional[List[str]] = None,
                    ignore_case: bool = False) -> str:
        """Format all fields of the BibItem for display in the terminal,
        such as in the `show` command.

        Args:
            has_file (bool): Indicates whether there is a local fulltext file present.
            patterns (list[str]): List of patterns to highlight.
            ignore_case (bool): Whether matching for patterns should be case insensitive search. Default false.

        Returns:
            Formatted string with all fields.
        """
        title = tex2term(self.get('title', 'Unknown title'))
        info_lines = textwrap.wrap(title)
        if patterns:
            info_lines = [highlight(line, patterns, ignore_case) for line in info_lines]
        if 'author' in self:
            authors_string = self['author'] if len(self['author']) < 67 \
                                            else self.authors[0] + ' et al.'
            author_line = '{}: {}'.format(_c('Author(s)', 'r'), tex2term(authors_string))
            if patterns:
                author_line = highlight(author_line, patterns, ignore_case)
            info_lines.append(author_line)
        if 'doi' in self:
            doi_line = str(_c('doi:'+self['doi'], 'y'))
            if patterns:
                doi_line = highlight(doi_line, patterns, ignore_case)
            info_lines.append(doi_line)
        start_line = str(_c(self['ID'], 'm'))+(' [local file]' if has_file else '')
        return '\n'.join([start_line]+list(indented(info_lines)))

    @property
    def authors(self) -> List[str]:
        return re.split(r'\s(?:and|AND)\s', self['author'])

    def pdf_path(self, bib_files_path: Path) -> Path:
        return bib_files_path/(self['ID']+'.pdf')

    def format_detail(self, format_type: Literal['simple', 'bibtex'] = 'simple') -> str:
        """Format all fields of the BibItem for detailed display.

        Args:
            format_type: 'simple' for key-value list, 'bibtex' for raw BibTeX.

        Returns:
            Formatted string with all fields.
        """
        if format_type == 'bibtex':
            return dumps({self['ID']: dict(self)})

        lines = [f"\n{self['ID']} ({self['ENTRYTYPE']})\n"]
        for key, value in sorted(self.items()):
            if key.islower():
                lines.append(f'{key.capitalize()}: {value}')
        return '\n'.join(lines)



class Bibliography:
    """A class to manage bibliographic data in a database.
    It mimics a dictionary with bibtex ids as keys and
    returns a BibItem, which is also dictionary-like.
    Technically it is a wrapper around the dbm.gnu database.
    """

    def __init__(self, path: Union[Path, str], mode: str = 'r') -> None:
        self.mode = mode

        self.path = Path(path)

        self.db = shelve.open(str(self.path), mode)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

    def __getitem__(self, key: str):
        return BibItem(self.db[key])

    def __setitem__(self, key: str, bibitem: BibItem):
        self.db[key] = bibitem

    def __contains__(self, identifyer: str):
        return identifyer in self.ids()

    def __len__(self):
        return len(self.db)

    def __iter__(self):
        return self.ids()

    def __str__(self):
        return '\n'.join(str(self[key]) for key in self)

    def update(self, data):
        """Add entries to the bibliography.

        Arguments:
            data: Can be a BibTeX string, a Bibliography, or a dict from parser.loads()

        Returns:
            List of added entry IDs.
        """
        added_keys = []
        if isinstance(data, str):
            entries = loads(data)
            for key, entry in entries.items():
                self[key] = BibItem(entry)
                added_keys.append(key)
        elif isinstance(data, Bibliography):
            for key in data.ids():
                self[key] = data[key]
                added_keys.append(key)
        elif isinstance(data, dict):
            for key, entry in data.items():
                self[key] = BibItem(entry)
                added_keys.append(key)
        else:
            raise TypeError(f'Cannot read {type(data)}, need str, Bibliography, or dict')
        return added_keys

    def remove(self, key: str):
        del self.db[key]

    def ids(self):
        """IDs in the bibliography. Similar to dict.keys."""
        yield from self.db.keys()

    def values(self):
        """Similar to dict.values.
        Returns list of BibItems."""
        yield from self.db.values()

    def items(self):
        """Similar to dict.items.
        Returns list of (ID, BibItem) tuples."""
        yield from self.db.items()

    def bibtex(self):
        """Returns a single string with the bibtex
        code of all items in the bibliography"""
        return dumps(self).strip()

    def search(self, patterns, ids_only=False, ignore_case: bool = False):
        """Find all matches of the pattern in the bibliography."""
        flags = re.IGNORECASE if ignore_case else 0
        if ids_only:
            for key in self.ids():
                if all(re.search(pat, key, flags) for pat in patterns):
                    yield self[key]
        else:
            for key, val in self.items():
                if all(any(re.search(pat, v, flags) for v in val.values())
                       for pat in patterns):
                    yield val

    def cleanup(self):
        """Try to reduce memory usage, by reorganizing
        database and deleting unnecessary fields"""
        pass # TODO: implement

    def close(self):
        self.db.close()
