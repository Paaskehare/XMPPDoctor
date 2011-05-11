MODULE_NAME = 'example'


class mod:
    def __init__(self, bot):
        self.bot = bot
        self.bot.register_cmd('example', self.test)
        self.bot.say('"%s" successfully loaded' % MODULE_NAME)

    def test(self, msg, cmd):
        self.bot.say('hej, du skrev: %s' % ' '.join(cmd[1:]))

