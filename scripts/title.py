#!/usr/bin/env python
# encoding: utf-8

import re
import html.parser
import json
from urllib.request import urlopen

MODULE_NAME = 'title'

def urlLookup(url):
    page = None
    TitlePattern = re.compile(b'<title.*>(.*?)<\/title>', re.I | re.S)
    try:
        page = urlopen(url)
    except:
        return

    finally:
        try:
            match = TitlePattern.search(page.read())
            page.close()
            if match:
                title = match.groups(0)[0].decode('utf-8').strip().replace('\n', ' ').replace('\r', '')
                h = html.parser.HTMLParser()

                if title:
                    return h.unescape(title)
                else:
                    return
        except AttributeError:
            return

def youtube(id):
    try:
        try:
            url = 'http://gdata.youtube.com/feeds/videos/%s?alt=json' % id
            page = urlopen(url)
        finally:
            entry = json.loads(page.read().decode('utf-8'))['entry']
            vid = {'title': entry['title']['$t'], 'category': entry['media$group']['media$category'][0]['label']}
            page.close()
            return '(%s) %s' % (vid['category'], vid['title'])
    except:
        return


class mod:
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_event_handler('groupchat_message', self.message)

    def message(self, msg):
        YouTubePattern = re.compile('http://(www\.)?youtube\.com/watch\?v=([a-zA-Z0-9\-_]{10,13})', re.I)
        match = re.search(r'((http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?)', msg['body'])


        nick = ''

        try:
            nick = str(msg['from']).split('/', 1)[1]
        except:
            pass

        if nick == self.bot.config().NICKNAME:
            match = None

        if match:
            url = match.groups(0)[0]

            title = ''

            yt = re.match(YouTubePattern, url)

            if yt:
                title = youtube(yt.groups(0)[1])
            else:
                title = urlLookup(url)

            if title:
                self.bot.say(title)
