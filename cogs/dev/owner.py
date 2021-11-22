from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.path = 'cogs.'

    @commands.command(name="load", hidden=True)
    @commands.has_permissions()
    @commands.is_owner()
    async def load(self, ctx, *, cog: str = None):
        cog = self.parse_args(cog)
        for module in cog:
            self.bot.load_extension(self.path + module)
        await ctx.send("**`SUCCESS`**")

    @commands.command(name="unload", hidden=True)
    @commands.has_permissions()
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str = None):
        cog = self.parse_args(cog)
        for module in cog:
            self.bot.unload_extension(self.path + module)
        await ctx.send("**`SUCCESS`**")

    @commands.command(name="reload", hidden=True)
    @commands.has_permissions()
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str = None):
        cog = self.parse_args(cog)
        for module in cog:
            self.bot.unload_extension(self.path + module)
            self.bot.load_extension(self.path + module)
        await ctx.send("**`SUCCESS`**")

    def parse_args(self, cog):
        if cog is None:
            cog = [cg for cg in
                    self.bot.config["extensions"]
                    if 'user' in cg]
            return cog

        if isinstance(cog, str):
            if ' ' in cog:
                raise ValueError('One module at a time!')
            if cog in ('owner', 'settings'):
                cog = 'dev.' + cog
            else:
                if 'user' not in cog:
                    cog = 'user.' + cog
            cog = [cog]
        return cog

    @reload.error
    @load.error
    @unload.error
    async def error(self, ctx, error):
        if isinstance(error, (commands.NotOwner,
                              commands.errors.CommandInvokeError)):
            await ctx.send(f"```ERROR: {error.__cause__}```")
        else:
            print(error)


def setup(bot):
    bot.add_cog(Owner(bot))
