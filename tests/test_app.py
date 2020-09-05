import pytest

from app.app import MagicJokeFromPolishLanguage
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mjfpl():
    mjfpl = MagicJokeFromPolishLanguage()
    return mjfpl

@pytest.mark.usefixtures("mjfpl")
class TestApp(object):

    alfabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",  "m", "n", "o",
               "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


    @pytest.mark.parametrize("basic_string, cutet_string",[("mucha","ucha"), ("kupa", "upa")])
    def test_compare_string_positive(self,basic_string, cutet_string, mjfpl):
        assert mjfpl.compare_string(basic_string, cutet_string)

    @pytest.mark.parametrize("basic_string, cutet_string",[("muchy","ucha"), ("alalala", "lalalal")])
    def test_compare_string_negative(self, basic_string, cutet_string, mjfpl):
        assert not mjfpl.compare_string(basic_string, cutet_string)

    def test_get_all_hrefs_from_page(self, mjfpl):
        returned_tested = mjfpl.get_all_hrefs_from_page()
        alfabet = ["a", "ą", "b", "c","ć", "d", "e","ę", "f", "g", "h", "i", "j", "k", "l","ł", "m", "n", "ń", "o", "ó",
                   "p", "q", "r", "s","ś", "t", "u", "v", "w", "x", "y", "z", "ź", "ż"]
        assert len(returned_tested) == 35
        guard = 0
        for _ in alfabet:
            assert "wszystkie-slowa-jezyka-polskiego.php?id=na-litere-{}".format(_) == returned_tested[guard]
            guard+=1

    def test_get_all_subhrefs_from_page(self, mjfpl):
        list_subhrefs = []
        for _ in self.alfabet:
            list_subhrefs.append("wszystkie-slowa-jezyka-polskiego.php?id=na-litere-{}".format(_))

        returned = mjfpl.get_all_subhrefs_from_page(list_subhrefs)
        assert len(returned) == 296

    def test_get_words(self, mjfpl):
        url = "wszystkie-slowa-jezyka-polskiego.php?id=6-literowe-na-litere-a"
        mjfpl.get_words(url)
        assert "abbami" in mjfpl.all_words
        assert "abacie" in mjfpl.all_words
        assert "ażurze" in mjfpl.all_words

    def test_clean_up_words(self, mjfpl):
        mjfpl.all_words = ["a","b","c","d","e","ab","bb","cb","db","eb", "abc","bbc","cbc","dbc","ebc",'ela','efa', 'eae']
        mjfpl.clean_up_word()
        assert mjfpl.liczba_wszystkich_slow == 15
        assert mjfpl.words_dict[1] == {'a': ['a'], 'b': ['b'], 'c': ['c'], 'd': ['d'], 'e': ['e']}
        assert mjfpl.words_dict[2] == {'a': ['ab'], 'b': ['bb'], 'c': ['cb'], 'd': ['db'], 'e': ['eb']}
        assert mjfpl.words_dict[3] == {'a': ['abc'], 'b': ['bbc'], 'c': ['cbc'], 'd': ['dbc'], 'e': ['eae', 'ebc', 'efa', 'ela']}

    def test_generator_joke(self, mjfpl):
        mjfpl.words_dict = {
            4 : {"a" : ["abia", "acad", "anal", "azja"],'u': ["ucha", "ucha", "unia"],'z': ["zeza", "zezy","zyzy"]},
            5 : {'m': [ "mucha","mysza", "mąka","mżyt"], 'a': ['alicj', 'amina', 'azika']}
        }
        mjfpl.liczba_slow = 100
        mjfpl.liczba_wszystkich_slow = 100
        with patch.object(mjfpl, "save_jokes") as jokes:
            mjfpl.generate_jokes()
            jokes.assert_called_once()

    def test_save_jokes(self, mjfpl):
        mjfpl.save_jokes(""""Jak jest mucha bez ucha ? \n m \n\n! """)

    @pytest.mark.parametrize("lista",([],["bbb"]))
    def test_merge_find_pos(self, lista, mjfpl):
        for litera in self.alfabet:
            mjfpl.all_words.append("a{}a".format(litera))
        mjfpl.all_words.extend(lista)
        assert mjfpl.merge_find(looking = "afa", lista_words = mjfpl.all_words)

    @pytest.mark.parametrize("lista, look",([
        (['ccc'], 'ccc'),
        (['ccc', 'lll'], 'ccc'),
        (['aaa', 'ccc', 'kkk'], 'ccc'),
        (['aaa', 'ccc', 'kkk', 'lll'], 'ccc'),
        (['aaa','ccc','kkk','mmm','zzz'], 'kkk'),
        (['aaa','ccc','kkk','mmm','zzz'], 'ccc'),
        (['aaa','ccc','kkk','lll','mmm','zzz'], 'kkk'),
        (['aaa','ccc','kkk','lll','mmm','zzz'], 'ccc'),
        (['aaa','ccc','kkk','lll','mmm','zzz'], 'zzz'),
        (['aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff', 'ggg', 'hhh', 'iii', 'jjj', 'kkk', 'lll', 'mmm', 'nnn', 'ooo',
          'ppp', 'qqq', 'rrr', 'sss', 'ttt', 'uuu', 'vvv', 'www', 'xxx', 'yyy', 'zzz'], 'ccc'),
        (['aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff', 'ggg', 'hhh', 'iii', 'jjj', 'kkk', 'lll', 'mmm', 'nnn', 'ooo',
          'ppp', 'qqq', 'rrr', 'sss', 'ttt', 'uuu', 'vvv', 'www', 'xxx', 'yyy', 'zzz'], 'xxx'),
    ]))
    def test_merge_find_lista_words_exactly_in_center(self, mjfpl, lista, look):
        assert mjfpl.merge_find(look, lista_words=lista)

    @pytest.mark.parametrize("lista",([],["baa"]))
    def test_merge_find_negative(self, lista, mjfpl):
        elo = []
        for litera in self.alfabet:
            mjfpl.all_words.append("a{}a".format(litera))
            elo.append("{}{}{}".format(litera,litera,litera))
        assert not mjfpl.merge_find(looking = "bbb", lista_words=mjfpl.all_words)

