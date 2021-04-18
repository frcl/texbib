from collections.abc import Iterable, Generator


TEX = {
    r'\textquotedblleft': '"',
    r'\textquotedblright': '"',
    r'\textemdash': '-',
    r'\ss': 'ß',
}


def tex2term(string: str) -> str:
    for tex, sub in TEX.items():
        string = string.replace(tex, sub)
    string = string.replace('{', '')
    string = string.replace('}', '')
    return string


def indented(lines: Iterable[str], width: int = 2) -> Generator[str]:
    indent = ' '*width
    for line in lines:
        yield indent + line
