from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.path = 'cogs.'

    @commands.command(name="load", hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        self.bot.load_extension(self.path + cog)
        await ctx.send("**`SUCCESS`**")

    @commands.command(name="unload", hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        self.bot.unload_extension(self.path + cog)
        await ctx.send("**`SUCCESS`**")

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        self.bot.unload_extension(self.path + cog)
        self.bot.load_extension(self.path + cog)
        await ctx.send("**`SUCCESS`**")

    @reload.error
    @load.error
    @unload.error
    async def error_owner(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(f"ERROR: {error}")


def setup(bot):
    bot.add_cog(Owner(bot))
