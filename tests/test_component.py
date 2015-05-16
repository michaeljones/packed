
from __future__ import unicode_literals, print_function

from unittest import TestCase

from packed import Elem, Component


class TestComponent(TestCase):

    def test_simple_component(self):

        class MyComponent(object):

            def render(self):
                return Elem('a')

        elem = Elem(MyComponent)

        expected = "<a />"

        self.assertEqual(elem.to_html(), expected)

    def test_text_component(self):

        class MyComponent(object):

            def render(self):
                return 'Just some text'

        elem = Elem(MyComponent)

        expected = 'Just some text'

        self.assertEqual(elem.to_html(), expected)

    def test_props(self):

        class MyComponent(Component):

            def render(self):
                return 'My test property value: %s' % self.props['test']

        elem = Elem(MyComponent, {'test': 'test_value'})

        expected = 'My test property value: test_value'

        self.assertEqual(elem.to_html(), expected)
