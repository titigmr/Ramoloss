import discord
from discord.ext import commands



class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.path = 'cogs.'

    @commands.command(name="load", hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(self.path + cog)
        except Exception as e:
            await ctx.send(f"**`ERROR: {e}`**")
        else:
            await ctx.send("**`SUCCESS`**")

    @commands.command(name="unload", hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        print(cog)
        try:
            self.bot.unload_extension(self.path + cog)
        except Exception as e:
            await ctx.send(f"**`ERROR: {e}`**")
        else:
            await ctx.send("**`SUCCESS`**")

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(self.path + cog)
            self.bot.load_extension(self.path + cog)
        except Exception as e:
            await ctx.send(f"**`ERROR: {e}`**")
        else:
            await ctx.send("**`SUCCESS`**")

def setup(bot):
    bot.add_cog(Owner(bot))