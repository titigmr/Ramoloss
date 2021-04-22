import discord
from discord.ext import commands


class John(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return

        if self.is_john(message.content):
            await message.reply('https://tenor.com/view/reggie-nintendo-no-gif-5495518',
            mention_author=True)

    def is_john(self, message):
        message = message.lower()
        verify = ["nul", 'lag', 'online', 'low tier']
        if any(e in message for e in verify):
            return True

def setup(bot):
    bot.add_cog(John(bot))