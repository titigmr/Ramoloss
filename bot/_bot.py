import os
from discord.ext.commands import Bot


class Ramoloss(Bot):
    def __init__(self, config, token, **kwargs):
        self.config = config
        self.discord_token = token
        os.environ["command_prefix"] = self.config["command_prefix"]
        super().__init__(
            command_prefix=self.config["command_prefix"],
            description=self.config["description"],
            **kwargs)

        for extension in self.config["extensions"]:
            self.load_extension('cogs.' + extension)

    async def on_ready(self):
        print((f'Logged in as {self.user} with extensions:'
              f'\n{" ".join(self.extensions).replace("cogs.", "")}'))

    def run(self, *args, **kwargs):
        super().run(self.discord_token, reconnect=True)
