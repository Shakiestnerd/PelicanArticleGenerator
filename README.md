# Pelican Article Generator

This application creates article stubs for writing blog posts using Pelican.

[Pelican](1) is a static web site generator.

This application is currently under development.

## What it does

You run `article.py`, fill in a few fields on the form, click the "Create" button and you have an empty article file that you can use to write your blog post.

This allows you to write out several article stubs and once, saving you time and helping you to plan your content more effectively.

## Assumptions and Conventions

### Categories

1. You are using the Pelican static site generator.
2. Article categories are folder names inside of your content folder.
3. The folders **'images', 'pages', and 'static'**, if found in your content folder, are ignored and not considered categories.

### Files

Article files are named with the following format:

> YYYY-MM-DD-document-title-separated-by-dashes
>
> **Example:** 2009-10-14-sugary-pecans-or-walnuts.md

Files are saved with these extensions:

- md: Markdown file
- rst: Restructured text file

### Article

Once an article is created, simply open the article in your favorite text editor and replace the "Insert article here" with your own amazing prose.

Sample Markdown Article:

```md
---

Title: Sample Article
Date: 2020-02-21
Category: Technology
Tags: python
Author: shakiestnerd
Status: draft
Summary:
---Insert article here.
```

[1]: https://blog.getpelican.com/ "Main Pelican Web Site"
