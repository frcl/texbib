"""This is the way of texbib to bring colored text on the screen
"""


ALIASES = {
    'red': ['r'],
    'blue': ['b'],
    'green': ['g'],
    'yellow': ['y'],
    'margenta': ['m'],
    'cyan': ['c'],
    'white': ['w'],
}


class ColoredText:
    """Class that provides coloing of text
    using the mapping in 'ColoredText.colors'
    by constructor

        colored = ColoredText(uncolored,color)

    """
    _a2c = {
        a: c for c in ALIASES for a in ALIASES[c]+[c]
    }
    _colors = {
        'red' : '\033[91m',
        'green' : '\033[92m',
        'yellow': '\033[93m',
        'blue' : '\033[94m',
        'margenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
    }
    _colorend = '\033[0m'

    def __init__(self, text, color):
        self._color = self._colors[self._a2c[color]]
        self._text = text

    def __repr__(self):
        return "'{}'".format(str(self))

    def __str__(self):
        return self._color + self._text + self._colorend

    @classmethod
    def set_colors(cls, color_dict):
        """Define new set of colors and colorcodes"""
        if isinstance(color_dict, dict):
            cls._colors = color_dict
        else:
            raise ValueError("Colors must be given in a dic_tionary")

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
