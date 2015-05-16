
Packed
======

.. image:: https://travis-ci.org/michaeljones/packed.svg?branch=master
    :target: https://travis-ci.org/michaeljones/packed

Packed provides `JSX <https://facebook.github.io/jsx/>`__-style syntax within
Python files. It provides a system for converting::

   @packed
   def tag(self):
       share = get_share_link()
       return <a href={share}>Share on internet</a>

To::

   @packed
   def tag(self):
      share = get_share_link()
      return Elem(
           'a',
           {
               'href': share,
           },
           'Share on internet',
       )

Which then renders to the appropriate HTML output when called.


Usage
-----

The module can be called from the command line to find files with the **Packed**
syntax and convert them to pure Python. Files using the **Packed** syntax
should use the ``.pkd`` file extension. The command searches recursively through
the provided directory::

   python -m packed .

Will write pure Python ``.py`` files for all ``.pkd`` files under the current
directory.


Syntax
------

Packed supports basic HTML style syntax as well as creating your own custom tags
or components. The term ``component`` is taken from `React
<https://facebook.github.io/react/>`_. A ``component`` should have a ``render``
method which returns ``Elem`` instances which are created from the **Packed**
syntax.

For example::

   from packed import Component, packed

   class ShareLink(Component):

      def render(self):
         return <a href={self.props['link']}>Share on internet</a>

   @packed
   def tag(self):
       share = get_share_link()
       return <Share link={share} />

The ``Component`` base class exposes attributes passed in the HTML syntax as
entries in the ``props`` dictionary in a similar style to React.


Status
------

This software is in alpha. There is a series of tests which cover the currently
supported syntax. There are no nice error messages if things go wrong. Please
create issues with any syntax that is not handled properly.

Packed makes no effort to escape or make safe any content. I would particularly
welcome advice on this aspect.


Credits
-------

Packed uses the `pypeg2 <http://fdik.org/pyPEG/>`_ library for the parsing and
output of the Python files.

The idea is, of course, inspired by `JSX <https://facebook.github.io/jsx/>`_
from `Facebook <https://github.com/facebook>`_.

