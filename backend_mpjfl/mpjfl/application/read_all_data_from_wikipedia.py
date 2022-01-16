# coding=utf-8

"""
Class for download all nouns from this webpage:
https://pl.wiktionary.org/wiki/Kategoria:J%C4%99zyk_polski_-_rzeczowniki
And save to database:
"""

"""
Wejdz na strone 
Sparsuj ja
Pobierz wszystkie linki do slowek i do nastepnej strony
while: 
Idz na nastepna strone

"""

import requests
from bs4 import BeautifulSoup
from time import sleep

# from mpflj.model. import WordModel

from mpjfl.model.words_model import WordsModel

class FindAllWords:

    def __init__(self):
        self.go = True
        self.url = "https://pl.wiktionary.org/wiki/Kategoria:J%C4%99zyk_polski_-_rzeczowniki"
        self.url_to_regex = "https://pl.wiktionary.org/"
        self.links = [self.url]
        self.word_mapping = {}

    def get_all_next_page(self, tried ):
        """
        Method for get all page under hyperlink "nastepna strona"
        :return:
        """
        tried+=1
        print(tried)
        for tries in range(0,10):
            try:
                content = requests.get(self.url)
            except Exception as error:
                print("get_all_next_page", tries, error)
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
                    return self.get_all_next_page(tried)
                else:
                    return False
        return False

    def get_all_hyperlink_to_details_of_nouns(self):
        """
        Method to get all data about nouns onwebpage
        :return:
        """
        for each_link_to_next_page in self.links:
            print(each_link_to_next_page)
            for tries in range(0, 3):
                try:
                    content = requests.get(each_link_to_next_page)
                except Exception as error:
                    print("get_all_hyperlink_to_details_of_nouns", tries, error)
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

    # def get_nouns(self, url):
    #     for tries in range(0,3):
    #         try:
    #             content = requests.get(url)
    #         except Exception as error:
    #             print(tries, error)
    #             sleep(600)
    #         else:
    #             break
    #     text_to_soup = content.text
    #     soup = BeautifulSoup(text_to_soup, features="html.parser")
    #     livs = soup.find_all('a')
    #     for liv in livs:
    #         if liv.get("href") and "https" not in liv.get("href") and ":" not in liv.get("href"):
    #             if len(liv.text.split(" ")) == 1:
    #                 self.word_mapping[liv.text] = liv.get("href")
    #         elif "następna strona" in liv.text:
    #             new_url = self.url_to_regex + liv.get("href")
    #             if new_url not in self.links:
    #                 self.links.append(new_url)


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
            print(self.links[-1])
            self.links.remove(self.links[0])
            print(f"Done: {int(guard/309*100)}%")
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
            url = f"https://pl.wiktionary.org/{link}"
            for tries in range(0,3):
                print(f"{tries} for {link}")
                try:
                    content = requests.get(url)
                except Exception:
                    print(f"Can not download link: {url}")
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
                        print(word, " : ",mianownik_list, "NOT dopelniacz!")
                else:
                    for _ in range(0, len(mianownik_list)):
                        wm = WordsModel(mianownik_list[_],link, dopelniacz_list[_], len(mianownik_list[0]))
                        wm.save_to_db()

if __name__ == "__main__":
    faw = FindAllWords()
    a = faw.get_all_nouns_from_link()

