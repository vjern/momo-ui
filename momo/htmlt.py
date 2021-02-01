from typing import List
import re
from itertools import starmap


def pretty_html(html: str, verbose: bool = False) -> str:
    html = html.strip()
    html = re.sub(r'>\s+<', '><', html)
    depth = 0
    before = html[0]
    nhtml = [before]
    indent = 4
    space = ' '
    idx = 0
    inside_closing = False
    for idx, char in enumerate(html[1:]):
        # verbose and print(repr(html.strip()))
        # verbose and print(' ' * (idx) + '^', idx, len(html))
        if char == '>' and before != '/':
            nhtml.append(char)
            if not inside_closing:
                depth += 1
                # verbose and print('Y', f'{depth = }, {"".join(nhtml)!r}')
            else:
                inside_closing = False
            nhtml.append('\n' + indent * depth * space)
        elif char == '>' and before == '/':
            nhtml.append(char)
            nhtml.append('\n' + indent * depth * space)
        elif html[idx + 1:].startswith('</'):
            depth -= 1
            nhtml.append('\n' + indent * depth * space)
            # verbose and print('X', f'{depth = }, {"".join(nhtml)!r}')
            nhtml.append(char)
            inside_closing = True
        elif char == '\n':
            # nhtml.append(char)
            # nhtml.append(indent * depth * space)
            # verbose and print('Z', f'{depth = }, {"".join(nhtml)!r}')
            # verbose and print('ignored \\n')
            pass
        else:
            nhtml.append(char)
            # verbose and print(' ', f'{depth = }, {"".join(nhtml)!r}')
        before = char
    nhtml = ''.join(nhtml)
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
