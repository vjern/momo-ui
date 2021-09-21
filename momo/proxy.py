from .htmlt import tag


class HTMLProxyTyper:
    def __init__(self, proxy, type):
        self.proxy = proxy
        self.type = type


class HTMLProxy:

    __classes__ = []
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

        props = dict(self.props)

        # compiled_style = self.style + ';' + self.props.get('style', '')
        # compiled_style = compiled_style.strip(';')
        # props = self.props
        # if compiled_style:
        #     props = {**self.props, 'style': compiled_style}
        # elif 'style' in self.props:
        #     props.pop('style')

        props['style'] = (props.get('style', '') + ';' + self.style).strip(';')
        not props['style'] and props.pop('style')

        props['class'] = (props.get('class', '') + ' ' + ' '.join(set(self.__classes__))).strip()
        not props['class'] and props.pop('class')
        
        return tag(
            self.tag,
            self.get_content() or self.content,
            id=self.id,
            **props
        )

    def __and__(self, other: type):
        return HTMLProxyTyper(self, other)
