from flask import Flask
from typing import Callable, Any, Dict, List
from itertools import starmap
import uuid
import logging
from functools import partial



class HTMLProxy:

    def __init__(self, content: str = '', tag: str = 'div', style: str = '', **props):
        self.props = props
        self.tag = tag
        self.id = str(id(self))
        self.content = content
        self.style = style

    def get_content(self):
        pass

    def __repr__(self):
        return str(self)

    def __str__(self):
        compiled_style = self.style + ';' + self.props.get('style', '')
        compiled_style = compiled_style.strip(';')
        props = self.props
        if compiled_style:
            props = {**self.props, 'style': compiled_style}
        else:
            props.pop('style')
        return tag(self.tag, self.get_content() or self.content, id=self.id, **props)


def tag(tag: str, content: str = '', notail: bool = False, flags: List[str] = [], **kw) -> str:
    skw = ' '.join(starmap('{}={!r}'.format, kw.items()))
    skw = ' ' + skw if skw else skw
    sflag = ' '.join(flags)
    sflag = ' ' + sflag if sflag else sflag
    return f'<{tag}{skw}{sflag}>' + f'{content}</{tag}>' * (not notail)


class input(HTMLProxy):

    def __init__(self, placeholder: str = '', type: str = 'text', required: bool = False, **props):
        props = {
            **props,
            'type': type,
            'placeholder': placeholder
        }
        super().__init__(tag='input', notail=True, flags=['required'] * required, **props)


div = partial(HTMLProxy, tag='div')
button = partial(HTMLProxy, tag='button')


def interpret_layout(layout):
    return layout

def get_html(title: str, layout):
    return f"""
<!DOCTYPE html>
<html>
    <head>
        <title> {title} </title>
        <meta charset='UTF-8'>
    </head>
    <body>
        {interpret_layout(layout)}
    <style>
{open('style.css').read()}
    </style>
    </body>
</html>
    """


class Container:
    def __init__(self, *children):
        self.children = list(children)
    def append(self, child):
        self.children.append(child)
    def prepend(self, child):
        self.children.insert(0, child)


class Layout(Container, HTMLProxy):
    compstyle = ''
    axis = 'width'
    def __init__(self, *children):
        Container.__init__(self, *children)
        HTMLProxy.__init__(self)
        self.props['style'] = self.style
        self.props['class'] = 'layout ' + self.__class__.__name__.lower()
    def get_content(self):
        self.children = list(self.children)
        for child in self.children:
        #     # pass
            child.props['style'] = f'{self.compstyle}; {self.axis}: %.0f%%' % (95 / (len(self.children) or 1))
        logging.warning(f'{self.children = }')
        return ' '.join(map(str, self.children))


class layouts:
    class Column(Layout):
        axis = 'height'
        compstyle = 'display: block'
    class Line(Layout):
        compstyle = 'display: inline-block'

class Momo:

    def __init__(self):
        self.app = Flask(__name__)

    def page(self, route: str, title: str = None):
        def decorator(f):
            html = get_html(title=title or f.__name__, layout=f())
            @self.app.route(route)
            def wrapper(*a, **kw):
                return html
            return wrapper
        return decorator

    def run(self, *a, **kw):
        return self.app.run(*a, **kw)

    def call(self, f: Callable, args: Dict[str, Any]):
        # Check if endpoint exists for f, otherwise create it
        # endpoint = self.get_endpoint(f)
        pass
