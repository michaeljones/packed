
from unittest import TestCase

from pact import translate



class TestTranslate(TestCase):

    def test_translate(self):

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
                'class': "fa fa-twitter-square large-icon",
            },
        )
    )

"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)
