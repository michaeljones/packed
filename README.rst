
Packed
======

This is an attempt to introduce JSX-style syntax within Python files. It
provides a system for converting::

   def tag(self):
       twitter_share = get_twitter_link()
       return <a href={twitter_share}>Share on twitter</a>

To::

   def tag(self):
      twitter_share = get_twitter_link()
      return Elem(
           'a',
           {
               'href': twitter_share,
           },
           'Share on twitter',
       )

Which then renders to the appropriate HTML output when called.

The aim is to use it for Django template tags when only a small amount of html
is required and so inlining the HTML in the Python code might be preferable to
a separate template file.

Status
------

This software is in alpha. I don't know what I'm doing.

