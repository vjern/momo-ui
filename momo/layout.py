import logging

from .proxy import HTMLProxy


class Container:
    def __init__(self, *children):
        self.children = list(children)
    def append(self, child):
        self.children.append(child)
    def prepend(self, child):
        self.children.insert(0, child)
    def get_content(self):
        return ' '.join(map(str, self.children))


class Layout(Container, HTMLProxy):

    compstyle = 'display: initial'
    axis = 'width'

    def __init__(self, *children):
        Container.__init__(self, *children)
        HTMLProxy.__init__(self)
        self.props['style'] = self.style
        self.props['class'] = 'layout ' + self.__class__.__name__.lower()

    def get_content(self):
        self.children = list(self.children)
        for child in self.children:
            w = 95 / (len(self.children) or 1)
            child.props['style'] = f'{self.compstyle}; {self.axis}: {w:.0f}%'
        logging.warning(f'{self.children = }')
        return ' '.join(map(str, self.children))


class Column(Layout):
    axis = 'height'
    compstyle = 'display: block'


class Line(Layout):
    axis = 'width'
    compstyle = 'display: inline-block; height: 100%'
