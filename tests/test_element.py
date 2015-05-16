
from __future__ import unicode_literals, print_function

from unittest import TestCase

from pact import Elem


class TestElem(TestCase):

    def test_empty_elem(self):

        elem = Elem('a')

        expected = "<a />"

        self.assertEqual(elem.to_html(), expected)

    def test_elem(self):

        elem = Elem('a', {}, Elem('b', {}))

        expected = "<a><b /></a>"

        self.assertEqual(elem.to_html(), expected)

    def test_empty_elem_single_attribute(self):

        elem = Elem('a', {'class': 'some-icon'})

        expected = '<a class="some-icon" />'

        self.assertEqual(elem.to_html(), expected)

    def test_elem_single_attribute(self):

        elem = Elem('a', {'class': 'some-icon'}, Elem('b', {}))

        expected = '<a class="some-icon"><b /></a>'

        self.assertEqual(elem.to_html(), expected)

    def test_elem_multiple_attribute(self):

        elem = Elem('a', {'class': 'some-icon', 'data-width': 800}, Elem('b', {}))

        expected = '<a data-width="800" class="some-icon"><b /></a>'

        self.assertEqual(elem.to_html(), expected)

    def test_elem_with_text_child(self):

        elem = Elem('a', {}, 'My link text')

        expected = "<a>My link text</a>"

        self.assertEqual(elem.to_html(), expected)
