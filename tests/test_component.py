
from __future__ import unicode_literals, print_function

from unittest import TestCase

from packed import Elem


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
