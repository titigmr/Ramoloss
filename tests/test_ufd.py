from bot.cogs.utils import UltimateFD


class TestUFD:
    def test_char(self):
        ufd = UltimateFD()
        char = ufd.all_char
        assert 'wario' in list(char.keys())
        assert 'sora' in list(char.keys())
        assert 'donkey_kong' in list(char.keys())

    def test_move(self):
        pass

