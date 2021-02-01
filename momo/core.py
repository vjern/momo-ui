import sys
import json
from flask import Flask, request
from typing import Callable, Any, Dict, Union, List
import pathlib
from functools import partial
from contextlib import contextmanager

from .htmlt import pretty_html
from .jst import get_converter
from .proxy import HTMLProxy, HTMLProxyTyper
from .layout import Container, Layout


__module__ = sys.modules[__name__]
__folder__ = pathlib.Path(__file__).parent


@contextmanager
def Form():
    yield __module__


class Momo:

    def __init__(self):
        self.app = Flask(__name__, static_folder='static')
        self.endpoints = {}

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

    def ensure_endpoint(self, f):
        name = f.__name__
        endpoint = self.endpoints.get(name)
        if endpoint is None:
            endpoint = self.app.route(f'/{name}', methods=['POST'])(make_endpoint(f))
            self.endpoints = endpoint
        return name

    def call(self, f: Callable, args: Dict[str, Any] = None, output: HTMLProxy = None):
        # Check if endpoint exists for f, otherwise create it
        # endpoint = self.get_endpoint(f)

        call = f'http.summon("/{self.ensure_endpoint(f)}"'

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


def make_endpoint(f: Callable) -> Callable:
    def wrapper(*a):
        return {'result': f(*a, **request.json)}
    wrapper.__name__ = f'{f.__name__}_wrapper'
    return wrapper


class input(HTMLProxy):

    def __init__(self, placeholder: str = '', type: str = 'text', required: bool = False, **props):
        props = {
            **props,
            'type': type,
            'placeholder': placeholder
        }
        super().__init__(tag='input', notail=True, flags=['required'] * required, **props)


class select(Container, HTMLProxy):

    def __init__(self, options: Union[List[str], Dict[str, Any]], required: bool = False, **props):
        if isinstance(options, list):
            options = {o: o for o in options}
        HTMLProxy.__init__(self, tag='select', flags=['required'] * required, **props)
        Container.__init__(self, *(
            HTMLProxy(label, 'option', value=value)
            for value, label in options.items()
        ))
        self.options = options


div = partial(HTMLProxy, tag='div')
button = partial(HTMLProxy, tag='button')
submit = partial(input, type='submit')


def get_html(title: str, layout):
    html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title> {title} </title>
        <meta charset='UTF-8'/>
        <link href="/static/styles/style.css" rel="stylesheet"/>
    </head>
    <body>
    <script src="/static/scripts/http.js">
    </script>
        {layout}
    </body>
</html>
    """
    html = pretty_html(html)
    return html
