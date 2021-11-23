import json
import pytest
import discord
from bot import Ramoloss
import discord.ext.test as dpytest


with open('config.json', 'r', encoding='utf-8') as config_file:
    CONFIG = json.load(config_file)


@pytest.fixture
def bot_instance(event_loop):
    intents = discord.Intents.default()
    intents.members = True
    bot_ramoloss = Ramoloss(config=CONFIG,
                            token=None,
                            loop=event_loop,
                            intents=intents)
    dpytest.configure(bot_ramoloss)
    return bot_ramoloss


@pytest.mark.asyncio
async def test_ping(bot_instance):
    await dpytest.message("!hello")
    assert dpytest.verify().message().contains().content("Hello")