#!/usr/bin/env python
# encoding: utf-8

MODULE_NAME = 'lastfm'

import re
import html.parser
from urllib.request import urlopen

LASTFM_PATTERN = re.compile('<recenttracks user="(?P<username>\w+)".+<track nowplaying="true">.+<artist mbid=".+">(?P<artist>.+)<\/artist>.+<name>(?P<track>.+)<\/name>.+<\/track>.+<track>.+</track>', re.I | re.S)

def lastfm(user):
    url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&limit=1&api_key=b25b959554ed76058ac220b7b2e0a026' % user

    page = urlopen(url)

    m = LASTFM_PATTERN.search(str(page.read()))
    page.close()
    if m:
        return m.groupdict()
    else:
        return

class mod:
    def __init__(self, bot):
        self.bot = bot
        self.bot.register_cmd('np', self.lastfm)
        self.bot.register_cmd('gsp', self.grooveshark)

    def lastfm(self, msg, cmd):
        try:
            if cmd[1]:
                h = html.parser.HTMLParser()
                user = h.unescape(cmd[1])
        except IndexError:
            user = str(msg['from']).split('/')[1]


        try:
            info = lastfm(user)

            if info:
                self.bot.say('LastFM: %(artist)s - %(track)s' % info, msg['from'].bare)

        except:
            print('EXCEPTION!!!')

    def grooveshark(self, msg, cmd):

        h = html.parser.HTMLParser()

        try:
            if cmd[1]:
                user = h.unescape(cmd[1])
        except IndexError:
                user = str(msg['from']).split('/')[1]


        info = lastfm(user)

        if info:
            artist = h.unescape(info['artist'] + ' ' + info['track'])
            url = 'http://tinysong.com/a/%s?format=json&key=ce075ee5cd4917e5b0c909fa6fc2255c' % artist
            page = urlopen(url)
            p = str(page.read())
            res = p.replace('"', '').replace('\\', '')
            self.bot.say('LastFM: %s - %s @ %s' % (info['artist'], info['track'], res), msg['from'].bare)
