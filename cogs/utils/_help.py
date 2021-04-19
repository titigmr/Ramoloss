import discord

class HelperCommand:
    def __init__(self):
        pass

    def help(self, title, description_command):
        e = discord.Embed(title=title,
                        description=description_command)
        return e
