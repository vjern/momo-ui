import sys
import json
from flask import Flask
from typing import Callable, Any, Dict, List
from itertools import starmap
import uuid
import logging
from functools import partial
from contextlib import contextmanager


__module__ = sys.modules[__name__]


def get_converter(type: type) -> str:
    return {
        float: 'Number',
        int: 'Number'
    }.get(type, type.__name__)


@contextmanager
def Form():
    yield __module__


class HTMLProxyTyper:
    def __init__(self, proxy, type):
        self.proxy = proxy
        self.type = type


class HTMLProxy:

    valuename = 'value'

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

    def __and__(self, other: type):
        return HTMLProxyTyper(self, other)


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
submit = partial(input, type='submit')


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
    <script src="/static/scripts/http.js">
    </script>
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
            w = 95 / (len(self.children) or 1)
            child.props['style'] = f'{self.compstyle}; {self.axis}: {w:.0f}%'
        logging.warning(f'{self.children = }')
        return ' '.join(map(str, self.children))


class layouts:
    class Column(Layout):
        axis = 'height'
        compstyle = 'display: block'
    class Line(Layout):
        compstyle = 'display: inline-block; height: 100%'

class Momo:

    def __init__(self):
        self.app = Flask(__name__, static_folder='static')

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

    def call(self, f: Callable, args: Dict[str, Any] = None, output: HTMLProxy = None):
        # Check if endpoint exists for f, otherwise create it
        # endpoint = self.get_endpoint(f)

        call = f'http.summon("/{f.__name__}"'

        argv = []
        if args:
            for key, value in args.items():
                if isinstance(value, HTMLProxy):
                    value = f'document.getElementById("{value.id}").{value.valuename}'
                elif isinstance(value, HTMLProxyTyper):
                    value = f'{get_converter(value.type)}(document.getElementById("{value.proxy.id}").{value.proxy.valuename})'

                else:
                    value = json.dumps(value)
                argv.append(f'{key}: {value}')
        call += ', {%s}' % ', '.join(argv)

        if output:
            call += f', "{output.id}"'

        call += ')'

        return call
