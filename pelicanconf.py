#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Erik Johnson'
SITENAME = u'TerminalMage dot NET'
SITEURL = ''

TIMEZONE = 'America/Chicago'

THEME = '/home/erik/pelican/themes/pelican-bootstrap3'
BOOTSTRAP_THEME = 'slate'
PYGMENTS_STYLE = 'solarizeddark'
DEFAULT_LANG = u'en'
CC_LICENSE = 'CC-BY-SA'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Links
LINKS = (
    ('SaltStack', 'http://saltstack.com/'),
)

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/terminalmage'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Custom CSS for pelican-bootsrap3
#CUSTOM_CSS = 'static/custom.css'

# Tell Pelican to add 'extra/custom.css' to the output dir
#STATIC_PATHS = ['images', 'extra/custom.css']

# Tell Pelican to change the path to 'static/custom.css' in the output dir
#EXTRA_PATH_METADATA = {
#        'extra/custom.css': {'path': 'static/custom.css'}
#}
