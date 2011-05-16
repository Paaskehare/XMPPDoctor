#!/usr/bin/python
# coding: utf-8

SERVER = 'server.example.org', 5222

# Nickname of the bot
NICKNAME = 'Doctor'

# List of channels to join on connect
MUC_CHANNELS = [
  'channel@conference.example.org',
]

# Plugins to load at startup
PLUGINS = [
  'title',
  'calc',
  'urban',
  'lastfm',
  'google',
]

''' DO NOT EDIT PAST THIS LINE '''
LOADED_PLUGINS = {}
