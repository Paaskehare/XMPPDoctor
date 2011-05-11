#!/usr/bin/env python
# encoding: utf-8

MODULE_NAME = 'urban'
from urllib.request import urlopen
from urllib.parse import urlencode
import json

class mod:
    def __init__(self, bot):
        self.bot = bot
        self.bot.register_cmd('urban', self.urban)

    def urban(self, msg, cmd):
        try:
            term = urlencode({'term': cmd[1]})
			
            url = 'http://www.urbandictionary.com/iphone/search/define?' + term
            page = urlopen(url)
            res = json.loads(page.read().decode('utf-8'))['list'][0]

            res['definition'] = res['definition'][:130]
            self.bot.say('Term: %(word)s Definition: %(definition)s' % res)
        except:
            self.bot.say('Does not compute')
