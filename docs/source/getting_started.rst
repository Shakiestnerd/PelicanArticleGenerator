***************
Getting Started
***************

Features
========

Article Generator creates blank blog articles with some basic elements filled in
for you on a `Pelican`_ static web site.

The articles are generated in your choice of `Markdown`_ or `Restructured Text`_ format.

More about `Mastering Markdown`_.

It fills in a selection of tags into the article file based on your input in the
"Create a new article" form.  

These tags include:

* Title: The title for your article
* Date: The date for the article (defaults to today's date)
* Category: The article category based on the sub-folder names underneath the content folder.
* Tags: A comma separated list of tags for your article.
* Author(s): The author or a comma separated list of authors.
* Status: Flag used by Pelican to determine the visibility of the article.
* Summary: An initial paragraph for your article.

There is an option to include a section for a food recipe as a kind of blog post.

Assumptions
===========

* You are using `Pelican`_ as a static web site generator.
* Your project structure is close to the default structure used by Pelican.


Installation
============

Right now, the project is available on Github.  It can be cloned by opening a 
terminal window on your computer.  Navigate to the folder where you want to clone
Article Generator and then issue the following command:

::

    $ git clone https://github.com/Shakiestnerd/PelicanArticleGenerator.git

.. _Pelican: http://docs.getpelican.com/en/stable/
.. _Markdown: https://daringfireball.net/projects/markdown/syntax
.. _Restructured Text: https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html
.. _Mastering Markdown: https://guides.github.com/features/mastering-markdown/