#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Erik Johnson'
SITENAME = u'TerminalMage dot NET'
SITEURL = 'http://terminalmage.net'

TIMEZONE = 'America/Chicago'

THEME = '/home/erik/pelican/themes/pelican-bootstrap3'
BOOTSTRAP_THEME = 'slate'
PYGMENTS_STYLE = 'solarizeddark'
DEFAULT_LANG = u'en'
CC_LICENSE = 'CC-BY-SA'

FEED_DOMAIN = 'http://feeds.terminalmage.net'
FEED_ALL_ATOM = 'feeds/atom'
FEED_ALL_RSS = 'feeds/rss'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'
TRANSLATION_FEED_ATOM = None

# Links
LINKS = (
    ('Feed (RSS)', '{0}/rss'.format(FEED_DOMAIN)),
    ('Feed (ATOM)', '{0}/atom'.format(FEED_DOMAIN)),
    ('SaltStack', 'http://saltstack.com/'),
)

# Social widget
SOCIAL = (
    ('Twitter', 'https://twitter.com/terminalmage'),
    ('Google+', 'https://plus.google.com/+ErikJohnson'),
)

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
