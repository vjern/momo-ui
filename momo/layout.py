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
        return ' '.join(map(str, self.children))


class Column(Layout):
    pass


class Line(Layout):
    pass