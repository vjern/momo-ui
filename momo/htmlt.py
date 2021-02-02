from typing import List
import re
from itertools import starmap


def pretty_html(html: str, verbose: bool = False) -> str:

    html = html.strip()
    html = re.sub(r'>\s+<', '><', html)

    before = html[0]
    elements = [before]

    indent = 4
    space = ' '
    depth = 0
    inside_closing = False

    for idx, char in enumerate(html[1:]):
        if char == '>' and before != '/':
            elements.append(char)
            if not inside_closing:
                depth += 1
            else:
                inside_closing = False
            elements.append('\n' + indent * depth * space)
        elif char == '>' and before == '/':
            elements.append(char)
            elements.append('\n' + indent * depth * space)
        elif html[idx + 1:].startswith('</'):
            depth -= 1
            elements.append('\n' + indent * depth * space)
            elements.append(char)
            inside_closing = True
        elif char == '\n':
            pass
        else:
            elements.append(char)
        before = char

    nhtml = ''.join(elements)
    nhtml = re.sub(r'\n\s*\n', '\n', nhtml)
    nhtml = nhtml.strip()

    return nhtml


def tag(tag: str, content: str = '', notail: bool = False, flags: List[str] = [], **kw) -> str:
    skw = ' '.join(starmap('{}={!r}'.format, kw.items()))
    skw = ' ' + skw if skw else skw
    sflag = ' '.join(flags)
    sflag = ' ' + sflag if sflag else sflag
    if notail:
        return f'<{tag}{skw}{sflag}/>'
    return f'<{tag}{skw}{sflag}>' + f'{content}</{tag}>'
