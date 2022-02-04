# coding=utf-8

"""
Class for download all nouns from this webpage:
https://pl.wiktionary.org/wiki/Kategoria:J%C4%99zyk_polski_-_rzeczowniki
And save to database:
"""

"""

"""

import requests
from bs4 import BeautifulSoup
from time import sleep

from mjfpl.model.words_model import WordsModel

class FindAllWords:

    def __init__(self):
        self.go = True
        self.url = "https://pl.wiktionary.org/wiki/Kategoria:J%C4%99zyk_polski_-_rzeczowniki"
        self.url_to_regex = "https://pl.wiktionary.org/"
        self.links = [self.url]
        self.word_mapping = {}

    def get_all_next_page(self):
        """
        Method for get all page under hyperlink "nastepna strona"
        :return:
        """
        for tries in range(0,10):
            try:
                content = requests.get(self.url)
            except Exception as error:
                sleep(60)
            else:
                break
        text_to_soup = content.text
        soup = BeautifulSoup(text_to_soup, features="html.parser")
        livs = soup.find_all('a')
        for liv in livs:
            if "następna strona" in liv.text:
                new_url = self.url_to_regex + liv.get("href")
                if new_url not in self.links:
                    self.links.append(new_url)
                    self.url = new_url
                    # return self.get_all_next_page()
                else:
                    return False
        return False

    def get_all_hyperlink_to_details_of_nouns(self):
        """
        Method to get all data about nouns onwebpage
        :return:
        """
        for each_link_to_next_page in self.links:
            for tries in range(0, 3):
                try:
                    content = requests.get(each_link_to_next_page)
                except Exception as error:
                    sleep(60)
                else:
                    break
            text_to_soup = content.text
            soup = BeautifulSoup(text_to_soup, features="html.parser")
            livs = soup.find_all('a')
            for liv in livs:
                if liv.get("href") and "https" not in liv.get("href") and ":" not in liv.get("href"):
                    if len(liv.text.split(" ")) == 1:
                        self.word_mapping[liv.text] = liv.get("href")


    def get_all_nouns_from_link(self):
        """
        Method to get all nouns from links
        :return:
        """
        guard = 0
        while self.go:
            try:
                looked_url = self.links[0]
                self.get_nouns(looked_url)
            except IndexError:
                break
            guard+=1
            self.links.remove(self.links[0])
            if guard/309*100 > 101:
                break

        self.add_nouns_to_database()
        sleep(1)

    def add_nouns_to_database(self):
        """
        Method to iterate by all links and get nouns and genitive
        https://pl.wiktionary.org/wiki/abroseksualizm#pl
        """
        for word, link in self.word_mapping.items():
            print(word, link)
            url = f"https://pl.wiktionary.org/{link}"
            for tries in range(0,3):
                try:
                    content = requests.get(url)
                except Exception:
                    sleep(600) #wait 10 minut
                else:
                    break
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
                if len(words_list[mianownik_index:dopelniacz_index]) != len(words_list[dopelniacz_index:celownik_index]):
                    if dopelniacz_list:
                        dopelniacz_list.append(dopelniacz_list[-1])
                    else:
                        continue
                else:
                    for _ in range(0, len(mianownik_list)):
                        wm = WordsModel(mianownik_list[_],link, dopelniacz_list[_], len(mianownik_list[0]))
                        wm.save_to_db()

if __name__ == "__main__":
    faw = FindAllWords()
    a = faw.get_all_nouns_from_link()

