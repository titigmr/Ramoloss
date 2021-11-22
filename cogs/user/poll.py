import discord
from discord.ext import commands
from cogs.utils import EMOJI, HelperCommand, ParseArgs, TITLE_POLL, DESCRIPTION_COMMAND_POLL


class Poll(commands.Cog, HelperCommand, ParseArgs):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command(name="poll")
    async def poll(self, ctx):
        message = ctx.message
        if not message.author.bot:
            message_content = message.clean_content
            if message_content.find("{") == -1:
                if 'help' in message_content:
                    await ctx.send(embed=self.help(title=TITLE_POLL,
                                                   description_command=DESCRIPTION_COMMAND_POLL))
                else:
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')
                    await message.add_reaction('❔')
            else:
                title = f'{message.author.name} : '
                title += self.find_title(message_content)
                options = self.find_options(message_content, [])

                try:
                    poll_message = ""
                    for i, choice in enumerate(options):
                        if len(options) > 21:
                            await message.channel.send(("Please make sure you are using the"
                                                        "command correctly and have less than 21 options."))
                            return
                        elif not i == len(options):
                            poll_message = poll_message + "\n\n" + \
                                EMOJI[i] + " " + choice

                    e = discord.Embed(title=f"**{title}**",
                                      description=poll_message,
                                      colour=0x83bae3)

                    poll_message = await message.channel.send(embed=e)

                    final_options = []
                    for i, choice in enumerate(options):
                        if not i == len(options):
                            final_options.append(choice)
                            await poll_message.add_reaction(EMOJI[i])
                    await ctx.message.delete()
                except KeyError:
                    return ("Please make sure you are using the format"
                            "'$poll {title} [Option1] [Option2] [Option 3]'")
        else:
            return


def setup(bot):
    bot.add_cog(Poll(bot))
