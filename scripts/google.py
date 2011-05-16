#!/usr/bin/env python
# encoding: utf-8

MODULE_NAME = 'google'
import json
from urllib.request import urlopen
from urllib.parse import urlencode
import html.parser

class mod:
    def __init__(self, bot):
        self.bot = bot
        self.bot.register_cmd('g', self.google)
        self.bot.register_cmd('google', self.google)

    def google(self, msg, cmd):
        try:
            query = urlencode({'q': ' '.join(cmd[1:])})
            page = urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query)
            result = json.loads(page.read().decode('utf-8'))['responseData']['results'][0]
            h = html.parser.HTMLParser()

            result['titleNoFormatting'] = h.unescape(result['titleNoFormatting'])
            self.bot.say('Google: %(titleNoFormatting)s - %(unescapedUrl)s' % result, msg['from'].bare)
        except:
            self.bot.say('No results returned.', msg['from'].bare)
