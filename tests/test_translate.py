
from __future__ import unicode_literals, print_function

from unittest import TestCase

from packed import translate


class TestTranslate(TestCase):

    def test_whitespace(self):

        code = """   """

        expected = code

        result = translate(code)

        self.assertMultiLineEqual(expected, result)

    def test_simple_code(self):

        code = """return True"""

        expected = code

        result = translate(code)

        self.assertMultiLineEqual(expected, result)

    def test_simple_element(self):

        code = """
@packed
def tag(self):
    twitter_share = ""
    return <a></a>
"""

        expected = """
@packed
def tag(self):
    twitter_share = ""
    return Elem('a')
"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)

    def test_empty_element(self):

        code = """
@packed
def tag(self):
    twitter_share = ""
    return <a />
"""

        expected = """
@packed
def tag(self):
    twitter_share = ""
    return Elem('a')
"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)

    def test_single_child_no_attributes(self):

        code = """
@packed
def tag(self):
    twitter_share = ""
    return <a><i></i></a>
"""

        expected = """
@packed
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
@packed
def tag(self):
    twitter_share = ""
    return <a href={twitter_share}><i class="fa fa-twitter-square large-icon"></i></a>
"""

        expected = """
@packed
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
@packed
def tag(self):
    twitter_share = ""
    return <a> <i></i> <b></b> </a>
"""

        expected = """
@packed
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
@packed
def tag(self):
    twitter_share = ""
    return <a href={twitter_share}>
            <i class="fa fa-twitter-square large-icon"></i>
            <i class="fa fa-facebook-square large-icon"></i>
        </a>
"""

        expected = """
@packed
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
@packed
def tag(self):
    twitter_share = ""
    return <a href={twitter_share}><i class="fa fa-twitter-square large-icon" /></a>
"""

        expected = """
@packed
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
@packed
def tag(self):
    twitter_share = ""
    return "This is a test of text"
"""

        expected = code
        result = translate(code)
        self.assertMultiLineEqual(expected, result)

    def test_text_in_tag(self):

        code = """
    return <a href={twitter_share}>My link text</a>
"""

        expected = """
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
    return <p>My paragraph with {target} and {anotherTarget}</p>
"""

        expected = """
    return Elem(
        'p',
        {},
        'My paragraph with ',
        target,
        ' and ',
        anotherTarget,
    )
"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)

    def test_double_attribute(self):

        code = """
    link = <a href={link.url} rel="nofollow">{link.display}</a>
    """

        expected = """
    link = Elem(
        'a',
        {
            'href': link.url,
            'rel': 'nofollow',
        },
        link.display,
    )
    """

        result = translate(code)

        self.assertMultiLineEqual(expected, result)

    def test_indentation(self):
        """Make sure we're attempting to pick up the indentation from the code we're reading"""

        code = """
            link = <a href={link.url} rel="nofollow">{link.display}</a>
            """

        expected = """
            link = Elem(
                'a',
                {
                    'href': link.url,
                    'rel': 'nofollow',
                },
                link.display,
            )
            """

        result = translate(code)

        self.assertMultiLineEqual(expected, result)


class TestComponentTranslate(TestCase):

    def test_simple_component(self):

        code = """
    return <ExampleComponent />
"""

        expected = """
    return Elem(ExampleComponent)
"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)

    def test_mixed_children(self):

        code = """
    return <a><b></b><ExampleComponent /></a>
"""

        expected = """
    return Elem(
        'a',
        {},
        Elem('b'),
        Elem(ExampleComponent),
    )
"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)
