
from __future__ import unicode_literals, print_function

import re

from pypeg2 import parse, List, word, name, endl, restline, maybe_some, optional, some

whitespace = re.compile(r'\s+')

class Import(List):
    grammar = 'import', name()

class Function(List):
    grammar = 'def', some(re.compile('(?s).+'))


class NonPactLine(List):
    grammar = re.compile('.+'), '\n'


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
        try:
            text, result = parser.parse(text, '<')
            text, tag = parser.parse(text, TagName)
            text, result = parser.parse(text, whitespace)
            text, result = parser.parse(text, TagAttributes)
            text, result = parser.parse(text, '>')
            text, result = parser.parse(text, maybe_some(Tag))
            text, result = parser.parse(text, '</')
            text, result = parser.parse(text, tag.name)
            text, result = parser.parse(text, '>')
        except SyntaxError, e:
            print('Caught', e, text)
            return text, e

        return text, result


class PactBlock(List):
    grammar = re.compile(r'[^<\n]+'), Tag


class File(List):
    grammar = maybe_some([
        '\n',
        PactBlock,
        NonPactLine,
    ])


text = u"""
def tag(self):
    twitter_share = ""
    return <a href={twitter_share}><i class="fa fa-twitter-square large-icon"></i></a>
"""

import pdb
# pdb.set_trace()
result = parse(text, File, whitespace=None)

for entry in result:
    print(entry)

