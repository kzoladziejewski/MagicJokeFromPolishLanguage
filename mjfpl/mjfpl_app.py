# coding=utf-8
"""
Class for download all nouns from this webpage:
https://pl.wiktionary.org/wiki/Kategoria:J%C4%99zyk_polski_-_rzeczowniki
And save to database.
"""
import datetime
import requests
import logging

from time import sleep

from bs4 import BeautifulSoup

from app.model.words_model import WordsModel
from app.model.jokes_model import JokeModel
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(filename=f'crawler_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.log',
                    level=logging.INFO,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

class MagicJokeFromPolishLanguage:

    def __init__(self):
        self.go = True
        self.url = "https://pl.wiktionary.org/wiki/Kategoria:J%C4%99zyk_polski_-_rzeczowniki"
        self.url_to_regex = "https://pl.wiktionary.org/"
        self.links = [self.url]
        self.word_mapping = {}

    def __get_content_from_url(self, url, tries=10, timeout=60):
        for nr_try in range(0,tries):
            try:
                content = requests.get(url)
                return content
            except Exception as error:
                logging.error(error)
                sleep(timeout)

    def get_all_next_page(self, elo = 0):
        """
        Method for get all pages under hyperlink "nastepna strona" on webpage
        :return:
        """
        if elo == 2:
            return False
        content = self.__get_content_from_url(self.url, 10, 60)
        text_to_soup = content.text
        soup = BeautifulSoup(text_to_soup, features="html.parser")
        livs = soup.find_all('a')
        for liv in livs:
            if "następna strona" in liv.text:
                new_url = self.url_to_regex + liv.get("href")
                if new_url not in self.links:
                    self.links.append(new_url)
                    logging.debug(f'Added new url link {new_url} to links')
                    self.url = new_url
                    logging.debug(f"Go to next page {new_url}")
                    return self.get_all_next_page(2)
                else:
                    logging.debug(f"Achieved last webpage {self.links[-1]}")
                    return True
        return False

    def get_all_hyperlink_to_details_of_nouns(self):
        """
        Method to get all data about nouns on webpage
        :return:
        """
        for each_link_to_next_page in self.links:
            content = self.__get_content_from_url(each_link_to_next_page, 3, 60)
            text_to_soup = content.text
            soup = BeautifulSoup(text_to_soup, features="html.parser")
            livs = soup.find_all('a')
            for liv in livs:
                if liv.get("href") and "https" not in liv.get("href") and ":" not in liv.get("href"):
                    if len(liv.text.split(" ")) == 1:
                        self.word_mapping[liv.text] = liv.get("href")

    def add_nouns_to_database(self):
        """
        Method to iterate by all links and get nouns and genitive
        https://pl.wiktionary.org/wiki/abroseksualizm#pl
        """
        for word, link in self.word_mapping.items():
            logging.info(f"Add {word} to {link}")
            url = f"https://pl.wiktionary.org/{link}"
            content = self.__get_content_from_url(url, 3, 600)
            # text_to_soup = content.text.encode('utf-8').decode('ascii', 'ignore')
            text_to_soup = content.text
            soup = BeautifulSoup(text_to_soup, features="html.parser")

            words_list = []
            for tr in soup.findAll('td'):
                words_list.append(tr.text)

            if "mianownik" in words_list:
                mianownik_index = words_list.index("mianownik")
                dopelniacz_index = words_list.index("dopełniacz")
                celownik_index = words_list.index("celownik")
                mianownik_list = words_list[mianownik_index:dopelniacz_index][1:]
                dopelniacz_list = words_list[dopelniacz_index:celownik_index][1:]
                if len(words_list[mianownik_index:dopelniacz_index]) != len(
                        words_list[dopelniacz_index:celownik_index]):
                    if dopelniacz_list:
                        dopelniacz_list.append(dopelniacz_list[-1])
                    else:
                        continue
                else:
                    for _ in range(0, len(mianownik_list)):
                        data = {
                            "nouns": mianownik_list[_],
                            "url": link,
                            "genitive": dopelniacz_list[_],
                            "len_word": len(mianownik_list[0])
                        }
                        add_word = requests.post(url='http://127.0.0.1:8080/word',data=data)
                        logging.info(f'Word is send to localhost with {add_word.status_code}')


if __name__ == "__main__":
    mjfpl = MagicJokeFromPolishLanguage()
    mjfpl.get_all_next_page()
    mjfpl.get_all_hyperlink_to_details_of_nouns()
    mjfpl.add_nouns_to_database()
