#!/usr/bin/python
# encoding: utf-8

import logging
import time
import config

import sleekxmpp

import sys

class PluginManager:
    def __init__(self, bot):
        self.bot = bot
        for plugin in config.PLUGINS:
            self.load(plugin)

    def load(self, plugin):
        try:
            try:
                mod = __import__('scripts.'+plugin, {}, {}, ['mod'], 0)
                config.LOADED_PLUGINS[plugin] = mod.mod(self.bot)
            finally:
                print('%s loaded successfully' % plugin)

        except ImportError:
            print('IE')
            return

    def unload(self, plugin):
        mod = 'scripts.' + plugin
        try:
            del sys.modules[mod]
            del config.LOADED_PLUGINS[plugin]
        except:
            pass

    def reload(self, plugin):
        self.unload(plugin)
        self.load(plugin)

class Doctor(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        plugin_config = {}

        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.muc = None
        self.muc_channels = config.MUC_CHANNELS
        self.nickname = config.NICKNAME
        self.commands = {}

        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)
        self.add_event_handler('groupchat_message', self.groupMessage)

    def config(self): return config

    def start(self, event):
        self.sendPresence()
        self.getRoster()

        self.muc = self.plugin['xep_0045']
        for channel in self.muc_channels:
            self.muc.joinMUC(channel, self.nickname)
        self.pm = PluginManager(self)

    def register_cmd(self, cmd, f):
        self.commands[cmd] = f

    def message(self, msg):
        if msg['body'].startswith('.'):
            cmd = msg['body'][1:].split(' ')
            if cmd[0] == 'load':
                self.pm.load(cmd[1])
            elif cmd[0] == 'reload':
                self.pm.reload(cmd[1])
            elif cmd[0] == 'unload':
                self.pm.unload(cmd[1])

    def groupMessage(self, msg):
        global LinkPattern

        if msg['body'].startswith('.'):
            cmd = msg['body'][1:].split(' ')
            try:
                self.commands[cmd[0]](msg, cmd)
            except:
                pass

    def say(self, body, to=''):
        if not to: to=self.muc_rooms[0]
        msg = sleekxmpp.Message()
        msg['type'] = 'groupchat'
        msg['to'] = to
        msg['from'] = msg['to']
        msg['body'] = '→ %s' % body
        self.send(msg)

if __name__ == '__main__':
    logging.basicConfig(level='DEBUG', format='%(levelname)-8s %(message)s')

    xmpp = Doctor("Doctor", "somePass")

    xmpp.registerPlugin('xep_0030') # Service Discovery
    xmpp.registerPlugin('xep_0004') # Data Forms
    xmpp.registerPlugin('xep_0199') # XMPP Ping
    xmpp.registerPlugin('xep_0045') # XMPP MUC

    if xmpp.connect(config.SERVER):
        xmpp.process(threaded=True)
		
        print('Done')
    else:
        print('unable to connect')
