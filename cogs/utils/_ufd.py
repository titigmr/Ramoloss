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

DEFAULT_STATS = ["startup", "advantage",
                 "totalframes", "basedamage", "shieldstun"]

DEFAULT_EXCLUDE_OVERALL_STATS = ["Stats", "Initial Dash", 'Walk Speed',
                                 "SH / FH / SHFF / FHFF Frames", 'Shield Drop', 'Jump Squat']



class UltimateFD:
    def __init__(self, character, moves,
                 args_stats=None,
                 get_hitbox=False,
                 exclude_stats=['movename',
                                'whichhitbox', 'notes'],
                 exclude_moves=['dodge']):

        self.out = exclude_moves
        self.exclude_stats = exclude_stats
        self.args_stats = args_stats
        self.image = get_hitbox
        self.url = "https://ultimateframedata.com/"
        self.stats = {}
        self.avalaible_stats = {}
        self.REF_ATK = REF_ATK

        if self.args_stats is None:
            self.args_stats = DEFAULT_STATS

        if character is None:
            return

        if moves == 'all':
            moves = list(REF_ATK.keys())

        for move in moves:
            self._st_move = self._get_character_moves(
                name=character, move=move)

            stats = self._get_stats_move(
                self._st_move, self.image, *self.args_stats)
            self.stats.update(stats)

        if len(self.stats) == 0:
            raise KeyError(
                f'No moves found. Moves must be in: {list(REF_ATK.keys())}')

    def _get_soup(self, url):
        r = requests.get(url)
        if r.status_code != 200:
            all_char = self._get_all_characters(self.url)
            raise ValueError(
                f'Choose a valid character in: {list(all_char.keys())}')
        return BeautifulSoup(r.content, 'lxml')

    def _get_stats_move(self, stats_move, image, *kwargs):
        out_move = {}
        for m, s in stats_move.items():
            out_stats = {}
            available_stats = self._get_available_stats(
                st_move=s, exclude_stats=self.exclude_stats)
            self.avalaible_stats[m] = available_stats

            if self.args_stats == 'all':
                kwargs = available_stats

            if 'stats' in m:
                out_move[m] = self._format_overall_stats(s)
                continue

            if image:
                if 'hitbox' in available_stats:
                    if s.a is not None:
                        end_url_img = s.a["data-featherlight"]
                        url_img = self.url + end_url_img
                        out_stats['hitbox'] = url_img
                    available_stats.remove('hitbox')

            for arg in kwargs:
                if arg in available_stats:
                    val = self._format_stats(soup=s, class_name=arg)
                    out_stats[arg] = val
                else:
                    raise ValueError(
                        f'{arg} is not available. Make sure you are choosing in: {available_stats}')

            out_move[m] = out_stats
        return out_move

    def _format_stats(self, soup, class_name):
        soup = soup.find(class_=class_name)
        if soup is not None:
            return soup.text.strip()

    def _get_character_moves(self, name, move):
        url_char = self.url + name
        soup = self._get_soup(url_char)

        data_move = {mv.find(class_='movename').text.strip().lower():
                     mv for mv in soup.find_all(class_='movecontainer')
                     if mv.find(class_='movename') is not None}

        final_dict_move = {}
        for m_k, m_s in data_move.items():
            for out_word in self.out:
                if self._check_move(ref_atk=self.REF_ATK, move=move, m_k=m_k, out=out_word):
                    final_dict_move[m_k] = m_s
        return final_dict_move

    def _check_move(self, ref_atk, move, m_k, out):
        if move in ref_atk:
            if (ref_atk[move] in m_k):
                if (out not in m_k):
                    return True
        return False

    def _get_available_stats(self, st_move, exclude_stats):
        stats_list = set()

        for e in st_move.find_all('div'):
            if e.has_attr('class'):
                if len(e["class"]) != 0:
                    stats = " ".join(e['class'])
                    if stats not in exclude_stats:
                        stats_list.add(stats)
        return stats_list

    def _get_all_characters(self, url):
        soup = self._get_soup(url)
        characters = {}
        for i in soup.find_all('a'):
            href = i["href"]
            if ('.php' in href) and ('stats' not in href):
                name = href[1:].replace('.php', '')
                url_c = url + href
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