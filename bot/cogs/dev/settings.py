from discord.ext import commands


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello')
    async def say_hello(self, ctx):
        await ctx.channel.send(f'Hello {ctx.author.name}')


    @commands.has_permissions(administrator=True)
    @commands.command(name='set_prefix')
    async def set_prefix(self, ctx, *, new_prefix: str):
        self.bot.command_prefix = new_prefix
        await ctx.send(f'Prefix has been set to `{new_prefix}`.')


    @set_prefix.error
    async def pref_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(error)



def setup(bot):
    bot.add_cog(Settings(bot))
