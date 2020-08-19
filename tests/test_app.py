import pytest

from app.app import MagicJokeFromPolishLanguage

class TestApp:
    mjfpl = MagicJokeFromPolishLanguage()

    @pytest.mark.parametrize("basic_string, cutet_string",[("mucha","ucha"), ("kupa", "upa")])
    def test_compare_string_positive(self,basic_string, cutet_string):
        assert self.mjfpl.compare_string(basic_string, cutet_string) == True

    @pytest.mark.parametrize("basic_string, cutet_string",[("muchy","ucha"), ("alalala", "lalalal")])
    def test_compare_string_negative(self, basic_string, cutet_string):
        assert self.mjfpl.compare_string(basic_string, cutet_string) == False
