import pytest
import requests
import pathlib
from unittest.mock import patch, MagicMock, call
from mjfpl.src.application.read_all_data_from_wikipedia import FindAllWords
from mjfpl.src.model.words_model import WordsModel

class TestApp:

    @pytest.fixture(autouse=True)
    def faw(self):
        faw = FindAllWords()
        yield faw

    @pytest.mark.parametrize('html_file, expected_word', [('Page-start', 'adaptator'), ('Page-middle', 'abramowianin')])
    def test_application_collect_all_links(self, faw, html_file, expected_word):
        returned_object = MagicMock()
        html_file = pathlib.Path().cwd().joinpath("test_data").joinpath(f"{html_file}.htm")
        returned_object.text = open(html_file, 'r', encoding="utf-8").read()
        with patch.object(requests, 'get') as mocked_get:
            mocked_get.return_value = returned_object
            faw.get_all_next_page()
            assert len(faw.links) == 2
            assert expected_word in faw.links[-1]

    def test_get_all_nouns_from_webpage(self, faw):
        returned_object = MagicMock()
        html_file = pathlib.Path().cwd().joinpath("test_data").joinpath("Page-middle.htm")
        returned_object.text = open(html_file, 'r', encoding="utf-8").read()
        with patch.object(requests, 'get') as mocked_get:
            mocked_get.return_value = returned_object
            faw.get_all_hyperlink_to_details_of_nouns()
            assert '500+' in faw.word_mapping.keys()
            assert faw.word_mapping['500+'] == 'https://pl.wiktionary.org/wiki/500%2B#pl'
            assert len(faw.word_mapping.keys()) == 199

    @pytest.mark.parametrize('word, calls', [('a-moll', 3), ('Aalen', 1), ('abecadlarka', 2)])
    def test_get_all_types_nouns_from_webpage(self, faw, word, calls):
        html_file = pathlib.Path().cwd().joinpath("test_data").joinpath(
            f"{word} – Wikisłownik, wolny słownik wielojęzyczny.htm")
        returned_object = MagicMock()
        returned_object.text = open(html_file, 'r', encoding="utf-8").read()
        faw.word_mapping = {f'{word}': f'https://pl.wiktionary.org/wiki/{word}#pl'}
        with patch.object(requests, 'get') as mocked_get, patch.object(FindAllWords,
                                                                       'add_nouns_to_database') as mocked_add:
        # with patch.object(requests, 'get') as mocked_get:
            mocked_get.return_value = returned_object
            faw.get_all_nouns_from_link()
            assert mocked_add.call_count == calls

    def test_add_nouns_to_database(self, faw):
        class SimpleClass:
            def __init__(self, nominative, genitive, verb):
                self.nominative = nominative
                self.genitive = genitive
                self.verb = verb
        with patch.object(WordsModel, 'save_to_db') as mocked_save_to_db:
            faw.add_nouns_to_database(SimpleClass('abecadlarka', 'abecadlarki', 'jest'))

    @pytest.mark.parametrize('word, genitive', [('abarognozja', 'abarognozji')])
    def test_create_genitive(self, faw, word, genitive):
        assert faw.create_genitive(word) == genitive
