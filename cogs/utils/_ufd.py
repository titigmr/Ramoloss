import requests
from bs4 import BeautifulSoup


REF_ATK = {"ftilt": 'forward tilt',
           'utilt': 'up tilt',
           'dtilt': 'down tilt',
           'fsmash': 'forward smash',
           'dsmash': 'down smash',
           'upsmash': 'up smash',
           'nair': 'neutral air',
           'fair': 'forward air',
           'bair': 'back air',
           'uair': 'up air',
           'dair': 'down air',
           'nb': 'neutral b',
           'sb': 'side b',
           'ub': 'up b',
           'db': 'down b',
           'grab': 'grab',
           'jab': 'jab',
           'stats': 'stats',
           'da': 'dash attack'}

DEFAULT_STATS = ["startup", "advantage", "activeframes",
                 "totalframes", "basedamage", "shieldstun"]

DEFAULT_EXCLUDE_OVERALL_STATS = ['Stats', 'Initial Dash',
                                 'Walk Speed',
                                 'SH / FH / SHFF / FHFF Frames',
                                 'Shield Drop', 'Jump Squat']


class UltimateFD:
    def __init__(self,
                 character: str = None,
                 moves: str = None,
                 args_stats=None,
                 get_hitbox: bool = False,
                 exclude_stats: list = ['movename',
                                        'whichhitbox',
                                        'notes'],
                 exclude_moves: list = ['dodge']):

        self.char = character
        self.exclude_moves = exclude_moves
        self.exclude_stats = exclude_stats
        self.url = "https://ultimateframedata.com/"
        self.stats = {}
        self.all_char = self.get_all_characters(self.url)
        self.avalaible_stats = {}
        self.args_stats = DEFAULT_STATS if args_stats is None else args_stats

        if character is None:
            return

        moves = list(REF_ATK.keys()) if moves == 'all' else moves
        data_move = self.get_character_data(name=character)

        for move in moves:
            st_move = self.get_character_moves(data=data_move,
                                               move=move)

            stats = self.get_stats_move(st_move,
                                        get_hitbox,
                                        *self.args_stats)
            self.stats.update(stats)

        if not self.stats:
            list_moves = list(REF_ATK.keys())
            raise ValueError(f"No moves found. Moves must be in: {list_moves}")

    def _get_soup(self, url):
        """
        Request an url for a valid character
        """
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(
                f'Choose a valid character in: {list(self.all_char.keys())}')
        return BeautifulSoup(response.content, 'lxml')

    def get_stats_move(self, stats_move, image, *kwargs):
        out_move = {}

        for move, stats in stats_move.items():
            out_stats = {}
            available_stats = self._get_available_stats(st_move=stats)
            self.avalaible_stats[move] = available_stats

            if self.args_stats == 'all':
                kwargs = available_stats

            if 'stats' in move:
                out_move[move] = self._format_overall_stats(stats)
                continue

            if image:
                if 'hitbox' in available_stats:
                    if stats.a is not None:
                        end_url_img = stats.a["data-featherlight"]
                        url_img = self.url + end_url_img
                        out_stats['hitbox'] = url_img
                    available_stats.remove('hitbox')

            for arg in kwargs:
                if arg in available_stats:
                    val = self._format_stats(soup=stats,
                                             class_name=arg)
                    out_stats[arg] = val
            out_move[move] = out_stats
        return out_move

    @staticmethod
    def _format_stats(soup, class_name):
        soup = soup.find(class_=class_name)
        if soup is not None:
            return soup.text.strip()
        return None

    def get_character_data(self, name):
        """
        Get list characters moves
        """
        url_char = self.url + name
        soup = self._get_soup(url_char)

        # for each movename not None get key (name) and value (stats)
        data_move = {mv.find(class_='movename').text.strip().lower():
                     mv for mv in soup.find_all(class_='movecontainer')
                     if mv.find(class_='movename') is not None}
        return data_move

    def get_character_moves(self, data: dict, move: str):
        """
        Select move in data moves
        """
        selected_dict_move = {}

        # check if moves is in REF const and not in exclude moves
        for move_k, move_s in data.items():
            for excluded_move in self.exclude_moves:
                if self._check_move(move=move, move_k=move_k, out=excluded_move):
                    selected_dict_move[move_k] = move_s
        return selected_dict_move

    @staticmethod
    def _check_move(move: str, move_k: str, out: str):
        """
        Check for a move if:
            - is in REF_ATK moves
            - not in excluded moves
        Return:
        -------
            bool
        """
        if move in REF_ATK:
            if REF_ATK[move] in move_k:
                if out not in move_k:
                    return True
        return False

    def _get_available_stats(self, st_move):
        """
        Parse BeautiFullSoup object to a list of available stats
        """
        stats_list = set()

        for div in st_move.find_all('div'):
            if div.has_attr('class'):
                if len(div["class"]) != 0:
                    stats = " ".join(div['class'])
                    if stats not in self.exclude_stats:
                        stats_list.add(stats)
        return stats_list

    def get_all_characters(self, url):
        """
        Get list of all characters

        Return:
        ------
            - dict, {character: url, ...}
        """
        soup = self._get_soup(url)
        characters = {}

        for balise in soup.find_all('a'):
            href = balise["href"]
            # href contain character name (remove # or http values)
            if ('#' not in href) and ("http" not in href) and ('stats' not in href):
                name = href.replace('/', '')
                url_c = url + name
                characters[name] = url_c
        return characters

    def _format_overall_stats(self, soup):
        overall_stats = {}
        for st in soup.find_all('div'):
            if not any(check in st.text for check in DEFAULT_EXCLUDE_OVERALL_STATS):
                if ' — ' in st.text:
                    spiting_stats = st.text.split(" — ")
                    if len(spiting_stats) == 2:
                        name, value = spiting_stats
                        overall_stats[name] = value
                    else:
                        name = spiting_stats[0]
                        value = " ".join(spiting_stats[1:])
        return overall_stats
