import discord
from discord.ext import commands


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.emoji = [
            "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER E}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"
        ]

    def find_title(self, message):
        first = message.find('{') + 1
        last = message.find('}')
        if first == 0 or last == -1:
            return "Not using the command correctly"
        return message[first:last]

    # parses the options (recursively), which should be in between square brackets ('[ option n ]')
    def find_options(self, message, options):
        first = message.find('[') + 1
        last = message.find(']')
        if (first == 0 or last == -1):
            if len(options) < 2:
                return "Not using the command correctly"
            else:
                return options
        options.append(message[first:last])
        message = message[last+1:]
        return self.find_options(message, options)

    @commands.command(name="poll")
    async def poll(self, ctx):
        "Create a poll (use $poll help for using examples)."
        message = ctx.message
        if not message.author.bot:
            message_content = message.clean_content
            if message_content.find("{") == -1:
                if 'help' in message_content:
                    await ctx.send(embed=self.help())
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
                            await message.channel.send("Please make sure you are using the command correctly and have less than 21 options.")
                            return
                        elif not i == len(options):
                            poll_message = poll_message + "\n\n" + \
                                self.emoji[i] + " " + choice

                    e = discord.Embed(title=f"**{title}**",
                                      description=poll_message,
                                      colour=0x83bae3)

                    poll_message = await message.channel.send(embed=e)

                    final_options = []
                    for i, choice in enumerate(options):
                        if not i == len(options):
                            final_options.append(choice)
                            await poll_message.add_reaction(self.emoji[i])
                    await ctx.message.delete()
                except KeyError:
                    return "Please make sure you are using the format '$poll {title} [Option1] [Option2] [Option 3]'"
        else:
            return

    def help(self):
        title = "**Create a poll**"
        description_command = """
                                Create a simple poll.
                                $poll Kenshuri is a troll?

                                For advanced polls use the folowing syntax:
                                $poll {title} [Option1] [Option2] [Option 3] ...

                                Note: options are limited at 21.
                                """

        e = discord.Embed(title=title,
                        description=description_command)
        return e


def setup(bot):
    bot.add_cog(Poll(bot))
