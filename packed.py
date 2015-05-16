
from __future__ import unicode_literals, print_function

import inspect
import re

from pypeg2 import parse, compose, List, name, maybe_some, attr, optional, some, ignore, Symbol


__version__ = '0.1.0'


whitespace = re.compile(r'\s+')
text = re.compile(r'[^<]+')


class Whitespace(object):
    grammar = attr('value', whitespace)

    def compose(self, parser, indent=0):
        "Compress all whitespace to a single space (' ')"
        indent_str = indent * "    "
        return "{indent}' '".format(indent=indent_str)


class Text(object):
    grammar = attr('whitespace', optional(whitespace)), attr('value', re.compile(r'[^<{]+'))

    def compose(self, parser, indent=0):
        indent_str = indent * "    "
        return "{indent}'{whitespace}{value}'".format(
            indent=indent_str,
            whitespace=self.whitespace or '',
            value=self.value
        )


class String(object):
    grammar = '"', attr('value', re.compile(r'[^"]*')), '"'

    def compose(self, parser):
        return "'%s'" % self.value


class InlineCode(object):
    grammar = '{', attr('code', re.compile(r'[^}]*')), '}'

    def compose(self, parser, indent=0):
        indent_str = indent * "    "
        return "{indent}{code}".format(
            indent=indent_str,
            code=self.code
        )


class Attribute(object):
    grammar = name(), '=', attr('value', [String, InlineCode])

    def compose(self, parser, indent=0):
        indent_str = indent * "    "
        return "{indent}'{name}': {value},".format(
            indent=indent_str,
            name=self.name,
            value=self.value.compose(parser)
        )


class Attributes(List):
    grammar = optional(whitespace, some(Attribute))

    def compose(self, parser, followed_by_children, indent):
        indent_str = indent * "    "

        if not len(self):
            indented_paren = '{indent}{{}},\n'.format(indent=indent_str)
            return indented_paren if followed_by_children else ''

        text = []
        text.append('{indent}{{\n'.format(indent=indent_str))
        for entry in self:
            if not isinstance(entry, basestring):
                text.append(entry.compose(parser, indent=indent+1))
                text.append('\n')
        text.append('{indent}}},\n'.format(indent=indent_str))

        return ''.join(text)


class EmptyTag(object):

    grammar = '<', name(), attr('attributes', Attributes), ignore(whitespace), '/>'

    def get_name(self):
        return "'%s'" % self.name

    def compose(self, parser, indent=0, first=False):
        text = []

        indent_str = indent * int(not first) * "    "
        end_indent_str = indent * "    "
        indent_plus_str = (indent + 1) * "    "

        has_contents = bool(self.attributes)
        paren_sep = '\n' if has_contents else ''
        contents_sep = ',\n' if has_contents else ''

        text.append(
            "{indent}Elem({paren_sep}{indent_plus}{name}{contents_sep}".format(
                indent=indent_str,
                indent_plus=indent_plus_str if has_contents else '',
                name=self.get_name(),
                paren_sep=paren_sep,
                contents_sep=contents_sep,
            )
        )
        text.append(self.attributes.compose(parser, followed_by_children=False, indent=indent+1))
        text.append(
            "{indent})".format(
                indent=end_indent_str if has_contents else '',
            )
        )

        return ''.join(text)


class ComponentName(object):

    grammar = attr('first_letter', re.compile(r'[A-Z]')), attr('rest', Symbol)

    def compose(self):
        return self.first_letter + self.rest


class ComponentTag(EmptyTag):

    grammar = (
        '<', attr('name', ComponentName), attr('attributes', Attributes), ignore(whitespace), '/>'
    )

    def get_name(self):
        return self.name.compose()


class NonEmptyTag(object):

    @staticmethod
    def parse(parser, text, pos):
        result = NonEmptyTag()
        try:
            text, _ = parser.parse(text, '<')
            text, tag = parser.parse(text, Symbol)
            result.name = tag
            text, attributes = parser.parse(text, Attributes)
            result.attributes = attributes
            text, _ = parser.parse(text, '>')
            text, children = parser.parse(text, TagChildren)
            result.children = children
            text, _ = parser.parse(text, maybe_some(whitespace))
            text, _ = parser.parse(text, '</')
            text, _ = parser.parse(text, result.name)
            text, _ = parser.parse(text, '>')
        except SyntaxError, e:
            return text, e

        return text, result

    def compose(self, parser, indent=0, first=False):
        text = []

        indent_str = indent * int(not first) * "    "
        end_indent_str = indent * "    "
        indent_plus_str = (indent + 1) * "    "

        has_children = bool(self.children)
        has_attributes = bool(self.attributes)
        has_contents = has_children or has_attributes
        paren_sep = '\n' if has_contents else ''
        contents_sep = ',\n' if has_contents else ''

        text.append(
            "{indent}Elem({paren_sep}{indent_plus}'{name}'{contents_sep}".format(
                indent=indent_str,
                indent_plus=indent_plus_str if has_contents else '',
                name=self.name,
                paren_sep=paren_sep,
                contents_sep=contents_sep
            )
        )
        text.append(
            self.attributes.compose(parser, followed_by_children=has_children, indent=indent+1)
        )
        text.append(self.children.compose(parser, indent=indent+1))
        text.append(
            "{indent})".format(
                indent=end_indent_str if has_contents else '',
                )
            )

        return ''.join(text)


tags = [ComponentTag, NonEmptyTag, EmptyTag]


class TagChildren(List):

    grammar = maybe_some(tags + [Text, InlineCode, Whitespace])

    def compose(self, parser, indent=0):
        text = []
        for entry in self:
            # Skip pure whitespace
            text.append(entry.compose(parser, indent=indent))
            text.append(',\n')

        return ''.join(text)


class PactBlock(List):

    grammar = re.compile(r'[^<\n]+'), tags

    def compose(self, parser, attr_of=None):
        text = []
        for entry in self:
            if isinstance(entry, basestring):
                text.append(entry)
            else:
                text.append(entry.compose(parser, indent=1, first=True))

        return ''.join(text)


class NonPactLine(List):

    grammar = attr('content', re.compile('.*')), '\n'

    def compose(self, parser, attr_of=None):
        return '%s\n' % self.content


class File(List):
    grammar = maybe_some([
        PactBlock,
        NonPactLine,
    ])

    def compose(self, parser, attr_of=None):
        text = []
        for entry in self:
            text.append(entry.compose(parser))

        return ''.join(text)


def translate(code):
    result = parse(code, File, whitespace=None)
    return compose(result)


def format_attribute(key, value):
    return '{name}="{value}"'.format(name=key, value=value)


def to_html(entity):

    if hasattr(entity, 'to_html'):
        return entity.to_html()
    else:
        # Assume unicode string or compatible
        return unicode(entity)


class Elem(object):

    def __init__(self, name, attributes=None, *children):

        self.name = name
        self.attributes = attributes or {}
        self.children = children

    def to_html(self):

        # Handle components by instanciating them and calling their render method
        if inspect.isclass(self.name):
            assert not self.children
            instance = self.name(**self.attributes)

            output = instance.render()

            return to_html(output)

        attribute_text = ' '.join(
            map(
                lambda item: format_attribute(item[0], item[1]),
                self.attributes.iteritems()
            )
        )

        if attribute_text:
            attribute_text = ' ' + attribute_text

        if self.children:
            children_text = ''.join(map(lambda c: to_html(c), self.children))
            return "<{name}{attributes}>{children}</{name}>".format(
                name=self.name,
                attributes=attribute_text,
                children=children_text
            )
        else:
            return "<{name}{attributes} />".format(
                name=self.name,
                attributes=attribute_text
            )
