import pytest

from unittest.mock import patch
from unittest.mock import MagicMock

from ..application.read_all_data_from_wikipedia import FindAllWords
import requests
import pathlib
class TestChangePage:

    def test_get_all_links(self):
        """
        Test case to check if is possible to click next on webpage to change website
        """
        faw = FindAllWords()
        returned_object = MagicMock()
        html_file = pathlib.Path().cwd().joinpath("test_data").joinpath("Page-start.htm")

        returned_object.text = open(html_file, 'r', encoding="utf-8").read()
        with patch.object(requests, "get") as mocked_request:
            mocked_request.return_value = returned_object
            faw.get_all_next_page()
            assert len(faw.links) > 1