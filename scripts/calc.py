#!/usr/bin/env python
# encoding: utf-8

from urllib.parse import urlencode
from http.client import HTTPConnection

MODULE_NAME = 'calc'


class mod:
    def __init__(self, bot):
        self.bot = bot
        self.bot.register_cmd('calc', self.calc)

    def calc(self, msg, cmd):
        expression = ' '.join(cmd[1:])
        query = urlencode({'q': expression})

        start = '<h2 class=r style="font-size:138%"><b>'
        end = '</b>'

        google = HTTPConnection("www.google.com")
        google.request("GET", "/search?num=1&"+query)

        page = google.getresponse()

        data = str(page.read())

        if data.find(start)==-1:
            self.bot.say('No results returned')
        else:
            begin=data.index(start)
            result=data[begin+len(start):begin+data[begin:].index(end)]
            result = result.replace('\\xa0', ',').replace('<font size=-2> </font>', ',').replace(' &#215; 10<sup>', 'E').replace('</sup>','')

            self.bot.say(result, msg['from'].bare)
