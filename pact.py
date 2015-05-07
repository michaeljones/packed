
from __future__ import unicode_literals, print_function

import re

from pypeg2 import parse, compose, List, word, name, endl, restline, maybe_some, optional, some


whitespace = re.compile(r'\s+')


class NonPactLine(List):
    grammar = re.compile('.*'), '\n'

    def compose(self, parser, attr_of=None):
        text = []
        for entry in self:
            text.append(entry)

        return '\n'.join(text)

class Attribute(List):
    grammar = name(), '=', re.compile(r'[^>]+')


class Attributes(List):
    grammar = maybe_some(Attribute)


class TagOpen(object):
    grammar = '<'


class TagClose(object):
    grammar = '>'


class TagAttributes(List):
    grammar = Attributes


class TagName(object):
    grammar = name()


class Tag(List):

    @staticmethod
    def parse(parser, text, pos):
        result = Tag()
        try:
            text, _ = parser.parse(text, '<')
            text, tag = parser.parse(text, TagName)
            result.name = tag.name
            text, _ = parser.parse(text, whitespace)
            text, _ = parser.parse(text, TagAttributes)
            text, _ = parser.parse(text, '>')
            text, children = parser.parse(text, TagChildren)
            result.append(children)
            text, _ = parser.parse(text, '</')
            text, _ = parser.parse(text, tag.name)
            text, _ = parser.parse(text, '>')
        except SyntaxError, e:
            return text, e

        return text, result

    def compose(self, parser, indent=0, first=False):
        text = []

        indent_str = indent * int(not first) * "    "
        end_indent_str = indent * "    "
        indent_plus_str = (indent + 1) * "    "

        text.append(
            "{indent}Elem(\n{indent_plus}'{name}'{sep}".format(**{
                'indent': indent_str,
                'indent_plus': indent_plus_str,
                'name': self.name,
                'sep': len(self) * ',\n'
            })
        )
        for entry in self:
            text.append(entry.compose(parser, indent=indent+1))
        text.append("{indent})\n".format(indent=end_indent_str))

        return ''.join(text)


class TagChildren(List):
    grammar = maybe_some(Tag)

    def compose(self, parser, indent=0):
        text = []
        for entry in self:
            text.append(entry.compose(parser, indent=indent))

        return '\n'.join(text)


class PactBlock(List):
    grammar = re.compile(r'[^<\n]+'), Tag

    def compose(self, parser, attr_of=None):
        text = []
        for entry in self:
            if isinstance(entry, basestring):
                text.append(entry)
            else:
                text.append(entry.compose(parser, indent=1, first=True))

        return ''.join(text)


class File(List):
    grammar = maybe_some([
        PactBlock,
        NonPactLine,
    ])

    def compose(self, parser, attr_of=None):
        text = []
        for entry in self:
            text.append(entry.compose(parser))

        return '\n'.join(text)


def translate(code):
    result = parse(code, File, whitespace=None)
    return compose(result)
