#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Dongweiming'
SITENAME = u'Diving into IPython notebook'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'cn'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('小明明s à domicile', 'http://www.dongwm.com/'),)

# Social widget
SOCIAL = (('github', 'https://github.com/dongweiming/'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = "pelican-themes/pelican-bootstrap3"

MARKUP = ('md', 'ipynb')

PLUGIN_PATHS = 'pelican-plugins'
PLUGINS = ['liquid_tags.include_code', 'liquid_tags.notebook', 'ipynb-reader']

NOTEBOOK_DIR = '/Users/dongweiming/diving_into_ipynb'

DEBUG = True
