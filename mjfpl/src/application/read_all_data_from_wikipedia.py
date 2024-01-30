# coding=utf-8
"""
Class for download all nouns from this webpage:
https://pl.wiktionary.org/wiki/Kategoria:J%C4%99zyk_polski_-_rzeczowniki
And save to database:
"""
import requests
import logging
import datetime

from time import sleep

from bs4 import BeautifulSoup
from mjfpl.src.model.words_model import WordsModel
logging.basicConfig(filename=f'read_all_data_from_wikipedia_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.log',
                    level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

class WordsMapping:
    def __init__(self, url):
        self.verb = None
        self.mianownik = None
        self.dopełniacz = None
        self.url = url

class FindAllWords:

    def __init__(self):
        self.go = True
        self.url = "https://pl.wiktionary.org/wiki/Kategoria:J%C4%99zyk_polski_-_rzeczowniki"
        self.url_to_regex = "https://pl.wiktionary.org/"
        self.links = [self.url]
        self.word_mapping = {}
    def exception_handler(self, url):
        for tries in range(0, 3):
            logging.info(f"Try nr {tries} to get content from {url}")
            try:
                content = requests.get(url)
                return content
            except Exception as error:
                logging.error(error)
                sleep(1)

    def get_all_next_page(self):
        """
        Method for get all page under hyperlink "nastepna strona"
        """
        content = self.exception_handler(self.url)
        text_to_soup = content.text
        soup = BeautifulSoup(text_to_soup, features="html.parser")
        livs = soup.find_all('a')
        for liv in livs:
            if "następna strona" in liv.text:
                new_url = self.url_to_regex + liv.get("href")
                if new_url not in self.links:
                    self.links.append(new_url)
                    self.url = new_url
                    logging.info(f"Go to next page {new_url}")
                    return self.get_all_next_page()
                return False

    def get_all_hyperlink_to_details_of_nouns(self):
        """
        Method to get all data about nouns on webpage
        """
        for each_link_to_next_page in self.links:
            content = self.exception_handler(each_link_to_next_page)
            text_to_soup = content.text
            soup = BeautifulSoup(text_to_soup, features="html.parser")
            livs = soup.find_all('a')
            for liv in livs:
                link_to_nouns = liv.get('href')
                title = liv.get('title')
                if link_to_nouns and title and len(title.split(' ')) == 1:
                    self.word_mapping[title] = link_to_nouns

    def get_all_nouns_from_link(self):
        """
        Method to get all nouns from links
        """
        for each_word, each_link in self.word_mapping.items():
            content = self.exception_handler(each_link)
            soup = BeautifulSoup(content.text, features="html.parser")
            table_soup = soup.find_all('table')
            for table in table_soup:
                if not 'mianownik' in table.text:
                    continue
                word_mapping_single = WordsMapping(each_link)
                word_mapping_multi = WordsMapping(each_link)
                rows = table.findChildren('tr')
                for row in rows:
                    columns = [column.text for column in row.findChildren('td')]
                    if columns:
                        setattr(word_mapping_single, columns[0], columns[1])
                        word_mapping_single.verb = 'jest'
                        if len(columns) == 3:
                            setattr(word_mapping_multi, columns[0], columns[2])
                            word_mapping_multi.verb = 'są'

                for words in [word_mapping_single, word_mapping_multi]:
                    if words.verb:
                        self.add_nouns_to_database(words)

    def create_genitive(self, word: str) -> str:
        """
        Method for create genitive from the nouns - in this case this is just simulate typical polish behaviour for
        change language
        :param word: word in noun form
        :return: str: word in genitive form
        """
        changing_letter_mapping = {'a': 'i'}
        ending_letter = word[-1]
        return word[:-1] + changing_letter_mapping.get(ending_letter)

    def add_nouns_to_database(self, words_mapping : 'WordsMapping'):
        """
        Method to iterate by all links and get nouns and genitive
        https://pl.wiktionary.org/wiki/abroseksualizm#pl
        """
        wm = WordsModel(**words_mapping.__dict__)
        wm.save_to_db()

if __name__ == "__main__":
    faw = FindAllWords()
    a = faw.get_all_nouns_from_link()
    # faw.get_all_next_page()
