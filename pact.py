
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


class Attribute(object):
    grammar = name(), '=', '{twitter_share}'


class Attributes(List):
    grammar = maybe_some(Attribute)


class Tag(List):
    grammar = '<', name(), whitespace, Attributes, '>'


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

