
from __future__ import unicode_literals, print_function

from unittest import TestCase

from pact import translate


class TestTranslate(TestCase):

    def test_simple_element(self):

        code = """
@pact
def tag(self):
    twitter_share = ""
    return <a></a>
"""

        expected = """
@pact
def tag(self):
    twitter_share = ""
    return Elem('a')
"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)

    def test_empty_element(self):

        code = """
@pact
def tag(self):
    twitter_share = ""
    return <a />
"""

        expected = """
@pact
def tag(self):
    twitter_share = ""
    return Elem('a')
"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)

    def test_single_child_no_attributes(self):

        code = """
@pact
def tag(self):
    twitter_share = ""
    return <a><i></i></a>
"""

        expected = """
@pact
def tag(self):
    twitter_share = ""
    return Elem(
        'a',
        {},
        Elem('i'),
    )
"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)

    def test_single_child(self):

        code = """
@pact
def tag(self):
    twitter_share = ""
    return <a href={twitter_share}><i class="fa fa-twitter-square large-icon"></i></a>
"""

        expected = """
@pact
def tag(self):
    twitter_share = ""
    return Elem(
        'a',
        {
            'href': twitter_share,
        },
        Elem(
            'i',
            {
                'class': 'fa fa-twitter-square large-icon',
            },
        ),
    )
"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)

    def test_simple_multiple_children(self):

        code = """
@pact
def tag(self):
    twitter_share = ""
    return <a> <i></i> <b></b> </a>
"""

        expected = """
@pact
def tag(self):
    twitter_share = ""
    return Elem(
        'a',
        {},
        ' ',
        Elem('i'),
        ' ',
        Elem('b'),
        ' ',
    )
"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)

    def test_multiple_children(self):

        code = """
@pact
def tag(self):
    twitter_share = ""
    return <a href={twitter_share}>
            <i class="fa fa-twitter-square large-icon"></i>
            <i class="fa fa-facebook-square large-icon"></i>
        </a>
"""

        expected = """
@pact
def tag(self):
    twitter_share = ""
    return Elem(
        'a',
        {
            'href': twitter_share,
        },
        ' ',
        Elem(
            'i',
            {
                'class': 'fa fa-twitter-square large-icon',
            },
        ),
        ' ',
        Elem(
            'i',
            {
                'class': 'fa fa-facebook-square large-icon',
            },
        ),
        ' ',
    )
"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)

    def test_empty_tag_translate(self):

        code = """
@pact
def tag(self):
    twitter_share = ""
    return <a href={twitter_share}><i class="fa fa-twitter-square large-icon" /></a>
"""

        expected = """
@pact
def tag(self):
    twitter_share = ""
    return Elem(
        'a',
        {
            'href': twitter_share,
        },
        Elem(
            'i',
            {
                'class': 'fa fa-twitter-square large-icon',
            },
        ),
    )
"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)

    def test_empty_text(self):

        code = ""
        expected = code
        result = translate(code)
        self.assertEqual(expected, result)

    def test_single_empty_line(self):

        code = "\n"
        expected = code
        result = translate(code)
        self.assertEqual(expected, result)

    def test_pure_text(self):

        code = """
@pact
def tag(self):
    twitter_share = ""
    return "This is a test of text"
"""

        expected = code
        result = translate(code)
        self.assertMultiLineEqual(expected, result)

    def test_text_in_tag(self):

        code = """
@pact
def tag(self):
    twitter_share = ""
    return <a href={twitter_share}>My link text</a>
"""

        expected = """
@pact
def tag(self):
    twitter_share = ""
    return Elem(
        'a',
        {
            'href': twitter_share,
        },
        'My link text',
    )
"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)

    def test_value_in_text(self):

        code = """
@pact
def tag(self):
    target = "home"
    return <a>My link to {target}</a>
"""

        expected = """
@pact
def tag(self):
    target = "home"
    return Elem(
        'a',
        {},
        'My link to ',
        target,
    )
"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)
