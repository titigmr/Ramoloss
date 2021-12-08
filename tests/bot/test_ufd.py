import json
import requests
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
    setattr(intents, 'members', True)
    bot_ramoloss = Ramoloss(config=config,
                            token=None,
                            loop=event_loop,
                            intents=intents)
    dpytest.configure(bot_ramoloss)
    return bot_ramoloss


class MockResponse:
    def __init__(self):
        self.status_code = 200
        self.content = MockResponse.open_file('wario')

    @staticmethod
    def open_file(filename):
        with open(f'save/{filename}.html', 'r', encoding='utf-8') as file:
            file_content = str(file.readlines())
        return file_content

    def get(self):
        return


def mock_get(*args, **kwargs):
    return MockResponse()


class TestUFD:
    def test_char(self, monkeypatch):
        """
        Test list of character is valid
        """
        monkeypatch.setattr(requests, 'get', mock_get)
        ufd = UltimateFD()
        char = list(ufd.get_all_characters(ufd.url).keys())
        assert 'wario' in char
        assert 'sora' in char
        assert 'donkey_kong' in char
        assert 'http' not in char

    def test_move(self, monkeypatch):
        monkeypatch.setattr(requests, "get", mock_get)
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


class TestDiscordUFD:
    @pytest.mark.asyncio
    async def test_move_command(self, bot_instance):
        await dpytest.message("!ufd list moves")
        description = dpytest.get_embed().description
        assert 'dair' in description
        assert 'fsmash' in description
        assert 'nb' in description

    @pytest.mark.asyncio
    async def test_char_command(self, bot_instance):
        await dpytest.message("!ufd list char")
        description = dpytest.get_embed().description
        assert 'wario' in description
        assert 'sora' in description
        assert 'captain_falcon' in description

    @pytest.mark.asyncio
    async def test_wario_command_title(self, bot_instance):
        await dpytest.message("!ufd wario ub")
        title = dpytest.get_embed().title
        assert 'Wario' in title
        assert 'Up B' in title

    async def test_wario_command_stats(self, bot_instance):
        await dpytest.message("!ufd wario ub")
        fields = dpytest.get_embed().fields
        assert 'Startup' in fields
        assert 'Shieldstun' in fields
