
from __future__ import unicode_literals, print_function

import re

from pypeg2 import parse, compose, List, word, name, endl, restline, maybe_some, optional, some

whitespace = re.compile(r'\s+')

class Import(List):
    grammar = 'import', name()

class Function(List):
    grammar = 'def', some(re.compile('(?s).+'))


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

    def compose(self, parser, attr_of=None):
        return self.name


class Tag(List):

    @staticmethod
    def parse(parser, text, pos):
        result = Tag()
        try:
            text, _ = parser.parse(text, '<')
            text, tag = parser.parse(text, TagName)
            result.append(tag)
            text, _ = parser.parse(text, whitespace)
            text, _ = parser.parse(text, TagAttributes)
            text, _ = parser.parse(text, '>')
            text, children = parser.parse(text, TagChildren)
            result.append(children)
            text, _ = parser.parse(text, '</')
            text, _ = parser.parse(text, tag.name)
            text, _ = parser.parse(text, '>')
        except SyntaxError, e:
            print('Caught', e, text)
            return text, e

        return text, result

    def compose(self, parser, attr_of=None):
        text = []
        for entry in self:
            if isinstance(entry, basestring):
                text.append(entry)
            else:
                text.append(entry.compose(parser))

        return '\n'.join(text)


class TagChildren(List):
    grammar = maybe_some(Tag)

    def compose(self, parser, attr_of=None):
        text = []
        for entry in self:
            text.append(entry.compose(parser))

        return '\n'.join(text)


class PactBlock(List):
    grammar = re.compile(r'[^<\n]+'), Tag

    def compose(self, parser, attr_of=None):
        text = []
        for entry in self:
            if isinstance(entry, basestring):
                text.append(entry)
            else:
                text.append(entry.compose(parser))

        return '\n'.join(text)


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


text = u"""
def tag(self):
    twitter_share = ""
    return <a href={twitter_share}><i class="fa fa-twitter-square large-icon"></i></a>
"""

import pdb
result = parse(text, File, whitespace=None)

for entry in result:
    print(entry)


# pdb.set_trace()
print(compose(result))
