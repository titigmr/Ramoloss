import discord
from discord.ext.commands import Bot

class Ramoloss(Bot):
    def __init__(self, config, token, extensions=None):
        self.config = config
        self.extensions_name = extensions
        self.discord_token = token
        super().__init__(
            command_prefix=config["command_prefix"],
            description=config["description"]
        )
        for extension in extensions:
            self.load_extension(extension)

    async def on_ready(self):
        print(f'Logged in as {self.user} with extensions: {" ; ".join(self.extensions_name).replace("cogs.","")}')

    def run(self):
        super().run(self.discord_token, reconnect=True)