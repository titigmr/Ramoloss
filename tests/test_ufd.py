import json
import pytest
import discord
import discord.ext.test as dpytest
from bot import Ramoloss
from bot.cogs.utils import UltimateFD, REF_ATK


class TestUFD:
    def test_char(self):
        """
        Test list of character is valid
        """
        ufd = UltimateFD()
        char = list(ufd.all_char.keys())
        assert 'wario' in char
        assert 'sora' in char
        assert 'donkey_kong' in char
        assert 'http' not in char

    def test_move(self):
        ufd = UltimateFD(character='wario',
                         moves='fair')
        move = ufd.stats
        assert any(REF_ATK["fair"] in key for key in move)

    def test_list_moves(self):
        ufd = UltimateFD(character='wario',
                         moves=['ub', 'nair'])
        move = ufd.stats
        assert any(REF_ATK["ub"] in key for key in move)
        assert any(REF_ATK["nair"] in key for key in move)


with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)


@pytest.fixture
def bot_instance(event_loop):
    intents = discord.Intents.default()
    intents.members = True
    bot_ramoloss = Ramoloss(config=config,
                            token=None,
                            loop=event_loop,
                            intents=intents)
    dpytest.configure(bot_ramoloss)
    return bot_ramoloss


@pytest.mark.asyncio
async def test_ping(bot_instance):
    await dpytest.message("!ufd wario nair")
    assert dpytest.verify().message().contains().content("Wario")
