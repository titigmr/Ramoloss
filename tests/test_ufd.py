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


