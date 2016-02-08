"""This is the way of texbib to bring colored text on the screen
"""

class ColoredText:
    """Class that provides coloing of text
    using the mapping in 'ColoredText.colors'
    by constructor

        colored = ColoredText(uncolored,color)

    """
    colors = {'ID': '\033[95m',   #margenta
              #'blue' : '\033[94m',
              #'green' : '\033[92m',
              'HL': '\033[93m'}      #yellow
    colorend = '\033[0m'

    def __init__(self, text, color):
        self.color = color
        self.text = text

    def __repr__(self):
        return "'{}'".format(str(self))

    def __str__(self):
        return self.colors[self.color] + self.text + self.colorend
