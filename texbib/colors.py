"""This is the way of texbib to bring colored text on the screen
"""

class ColoredText:
    """Class that provides coloing of text
    using the mapping in 'ColoredText.colors'
    by constructor

        colored = ColoredText(uncolored,color)

    """
    _colors = {'ID': '\033[95m',   #margenta
               #'blue' : '\033[94m',
               #'green' : '\033[92m',
               'HL': '\033[93m'}      #yellow
    _colorend = '\033[0m'

    def __init__(self, text, color):
        self.color = color
        self.text = text

    def __repr__(self):
        return "'{}'".format(str(self))

    def __str__(self):
        return self._colors[self.color] + self.text + self._colorend

    @classmethod
    def set_colors(cls, color_dict):
        """Define new set of colors and colorcodes"""
        if isinstance(color_dict, dict):
            cls.colors = color_dict
        else:
            raise ValueError("Colors must be given in a dic_tionary")
