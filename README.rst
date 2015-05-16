
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


Status
------

This software is in alpha. There is a series of tests which cover the currently
supported syntax. There are no nice error messages if things go wrong. Please
create issues with any syntax that is not handled properly.

Packed makes no effort to escape or make safe any content. I would particularly
welcome advice on this aspect.


Usage
-----

The module can be called from the command line to find files with the **Packed**
syntax and convert them to pure Python. Files using the **Packed** syntax
should use the ``.pyx`` file extension. The command searches recursively through
the provided directory::

   python -m packed .

Will write pure Python ``.py`` files for all ``.pyx`` files under the current
directory.


Syntax
~~~~~~

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


Use with Django
~~~~~~~~~~~~~~~

Here is an example of using **Packed** for a Django template tag to create a
list of links. This code replaces two template tags and two separate template
files::


   from django import template
   from packed import packed, Component, Elem
   register = template.Library()

   class Link(Component):

       def render(self):

           data = self.props['link']
           link = <a href={data['url']} rel="nofollow">{data['display']}</a>

           if data['type'] == 'facebook':
               icon = <i class="fa-li fa fa-facebook" />
           else:
               icon = <i class="fa-li fa fa-link"></i>

           return (
               <ul class="fa-ul">
                   <li>
                       {icon} {link}
                   </li>
               </ul>
           )

   @register.simple_tag
   @packed
   def format_links(entity_name, links):

       def to_link(link):
           return <Link link={link} />

       if links:
           return map(to_link, links)
       else:
           "We don't have any website links for {}".format(entity_name)


The ``format_links`` function returns a list of ``Link`` tags which are then
properly converted to a Python string of HTML tags by the work of the
preprocessor and the ``@packed`` decorator.


Credits
-------

Packed uses the `pypeg2 <http://fdik.org/pyPEG/>`_ library for the parsing and
output of the Python files.

The idea is, of course, inspired by `JSX <https://facebook.github.io/jsx/>`_
from `Facebook <https://github.com/facebook>`_.

