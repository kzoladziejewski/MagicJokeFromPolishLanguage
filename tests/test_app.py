import pytest

from app.app import MagicJokeFromPolishLanguage
from collections import defaultdict

class TestApp:
    mjfpl = MagicJokeFromPolishLanguage()

    alfabet = ["a", "ą", "b", "c", "ć", "d", "e", "ę", "f", "g", "h", "i", "j", "k", "l", "ł", "m", "n", "ń", "o", "ó",
               "p", "q", "r", "s",
               "ś", "t", "u", "v", "w", "x", "y", "z", "ź", "ż"]
    @pytest.mark.parametrize("basic_string, cutet_string",[("mucha","ucha"), ("kupa", "upa")])
    def test_compare_string_positive(self,basic_string, cutet_string):
        assert self.mjfpl.compare_string(basic_string, cutet_string) == True

    @pytest.mark.parametrize("basic_string, cutet_string",[("muchy","ucha"), ("alalala", "lalalal")])
    def test_compare_string_negative(self, basic_string, cutet_string):
        assert self.mjfpl.compare_string(basic_string, cutet_string) == False

    def test_get_all_hrefs_from_page(self):
        returned_tested = self.mjfpl.get_all_hrefs_from_page()
        assert len(returned_tested) == 35
        guard = 0
        for _ in self.alfabet:
            assert "wszystkie-slowa-jezyka-polskiego.php?id=na-litere-{}".format(_) == returned_tested[guard]
            guard+=1

    def test_get_all_subhrefs_from_page(self):
        list_subhrefs = []
        for _ in self.alfabet:
            list_subhrefs.append("wszystkie-slowa-jezyka-polskiego.php?id=na-litere-{}".format(_))

        returned = self.mjfpl.get_all_subhrefs_from_page(list_subhrefs)
        assert len(returned) == 370

    def test_get_words(self):
        url = "wszystkie-slowa-jezyka-polskiego.php?id=6-literowe-na-litere-a"
        self.mjfpl.get_words(url)
        assert "abbami" in self.mjfpl.all_words
        assert "abacie" in self.mjfpl.all_words
        assert "ażurze" in self.mjfpl.all_words

    def test_generator_joke(self):
        self.mjfpl.words_dict = defaultdict(list)
        self.mjfpl.liczba_slow = 100
        self.mjfpl.liczba_wszystkich_slow = 100
        self.mjfpl.words_dict[5].append("abbami")
        self.mjfpl.words_dict[4].append("bbami")
        self.mjfpl.words_dict[5].append("abacie")
        self.mjfpl.words_dict[4].append("bacie")
        self.mjfpl.words_dict[5].append("ażurze")
        self.mjfpl.words_dict[4].append("żurze")
        self.mjfpl.generate_jokes()

    def test_save_jokes(self):
        self.mjfpl.save_jokes(""""Jak jest mucha bez ucha ? \n m \n\n! """)

    def test_merge_find_pos_odd(self):
        new_list = []
        for litera in self.alfabet:
            self.mjfpl.all_words.append("a{}a".format(litera))
        for word in self.mjfpl.all_words:
            word = word.replace("ą","a").replace("ć","c").replace("ę","e").replace("ł","l").replace("ń","n").replace("ó",'o').replace("ż",'z').replace("ś","s").replace("ź","z")
            new_list.append(word)
        assert self.mjfpl.merge_find(looking = "afa", lista_words = new_list, index = len(self.mjfpl.all_words)) == True

    def test_merge_fin_pos_even(self):
        new_list = []
        for litera in self.alfabet:
            self.mjfpl.all_words.append("a{}a".format(litera))

        for word in self.mjfpl.all_words:
            word = word.replace("ą","a").replace("ć","c").replace("ę","e").replace("ł","l").replace("ń","n").replace("ó",'o').replace("ż",'z').replace("ś","s").replace("ź","z")
            new_list.append(word)
        new_list.append("bbb")
        assert self.mjfpl.merge_find(looking = "afa", lista_words = new_list, index = len(self.mjfpl.all_words)) == True


    def test_merge_find_negative(self):
        for litera in self.alfabet:
            self.mjfpl.all_words.append("a{}a".format(litera))
        assert self.mjfpl.merge_find(looking = "bbb", lista_words = self.mjfpl.all_words, index = len(self.mjfpl.all_words)) == False

