import json
import time
import pytest
import discord
import discord.ext.test as dpytest
from bot import Ramoloss
from bot.cogs.utils import UltimateFD, REF_ATK


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
        time.sleep(1)

    def test_move(self):
        ufd = UltimateFD(character='wario',
                         moves='fair')
        move = ufd.stats
        assert any(REF_ATK["fair"] in key for key in move)
        time.sleep(1)

    def test_list_moves(self):
        ufd = UltimateFD(character='wario',
                         moves=['ub', 'nair'])
        move = ufd.stats
        assert any(REF_ATK["ub"] in key for key in move)
        assert any(REF_ATK["nair"] in key for key in move)
        time.sleep(1)


class TestDiscordUFD:
    @pytest.mark.asyncio
    async def test_move_command(self, bot_instance):
        await dpytest.message("!ufd list moves")
        description = dpytest.get_embed().description
        assert 'dair' in description
        assert 'fsmash' in description
        assert 'nb' in description
        time.sleep(1)

    @pytest.mark.asyncio
    async def test_char_command(self, bot_instance):
        await dpytest.message("!ufd list char")
        description = dpytest.get_embed().description
        assert 'wario' in description
        assert 'sora' in description
        assert 'captain_falcon' in description
        time.sleep(1)

    @pytest.mark.asyncio
    async def test_wario_command_title(self, bot_instance):
        await dpytest.message("!ufd wario ub")
        title = dpytest.get_embed().title
        assert 'Wario' in title
        assert 'Up B' in title
        time.sleep(1)

    async def test_wario_command_stats(self, bot_instance):
        await dpytest.message("!ufd wario ub")
        fields = dpytest.get_embed().fields
        assert 'Startup' in fields
        assert 'Shieldstun' in fields
        time.sleep(1)
