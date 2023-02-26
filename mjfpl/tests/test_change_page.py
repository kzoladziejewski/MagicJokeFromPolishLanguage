import pytest

from unittest.mock import patch
from unittest.mock import MagicMock

from mjfpl.mjfpl_app import MagicJokeFromPolishLanguage

import requests
import pathlib

class TestChangePage:

    def test_get_all_links(self):
        """
        Test case to check if is possible to click next on webpage to change website
        """
        faw = MagicJokeFromPolishLanguage()
        returned_object = MagicMock()
        html_file = pathlib.Path(__file__).parent.joinpath("test_data").joinpath("Page-start.htm")

        returned_object.text = open(html_file, 'r', encoding="utf-8").read()
        with patch.object(requests, "get") as mocked_request:
            mocked_request.return_value = returned_object
            faw.get_all_next_page()
            assert len(faw.links) > 1

    def test_get_all_next_page(self):
        """
        Test case to check if is possible to get next webpage and url
        """
        faw = MagicJokeFromPolishLanguage()
        returned_object = MagicMock()
        html_file = pathlib.Path(__file__).parent.joinpath("test_data").joinpath("Page-start.htm")

        returned_object.text = open(html_file, 'r', encoding="utf-8").read()
        with patch.object(requests, "get") as mocked_request:
            mocked_request.return_value = returned_object
            faw.get_all_next_page()
