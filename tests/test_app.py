import pytest

from app.app import MagicJokeFromPolishLanguage

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
        self.mjfpl.all_words = ["abacie", "ażurze", "abbami", "bacie", "żurze", "bbami"]
        self.mjfpl.generate_jokes()
