import requests

from collections import defaultdict
from .models.word_model import WordModel
from .db import SessionLocal, engine, Base

class MagicJokeFromPolishLanguage:

    def __init__(self):
        self.base_url = "https://polski-slownik.pl/"
        self.base_page = "https://polski-slownik.pl/wszystkie-slowa-jezyka-polskiego.php"
        self.all_words = []
        self.jokes = []
        self.words_dict = defaultdict(list)
        self.liczba_slow = 0
        self.liczba_wszystkich_slow = 0

    def compare_string(self, basic_string, cutet_string):
        if basic_string[1:] == cutet_string:
            return True
        return False

    def get_all_hrefs_from_page(self):
        returned = requests.get(self.base_page).text
        returned = returned.split("\n")
        list_of_sub_url = []
        for element in returned:
                sub_url = self.__cut_url(element)
                if sub_url:
                    list_of_sub_url.append(sub_url)
        return list_of_sub_url

    def __cut_url(self, element):
        if "\" href=" in element and "favicon.ico" not in element and "title" not in element:
            sub_url = element[element.find("href=\""):element.find("class")]
            sub_url = sub_url.replace("href=", "").replace("\"", "").replace(" ", "")
            return sub_url

    def get_all_subhrefs_from_page(self, list_of_suburl):
        list_of_sub_url = []
        for url in list_of_suburl:
            print(self.base_url, url)
            returned= requests.get("{}{}".format(self.base_url, url)).text
            returned = returned.split("<td>")

            for element in returned:
                sub_url = self.__cut_url(element)
                if sub_url:
                    list_of_sub_url.append(sub_url)
        return list_of_sub_url

    def get_words(self, url_to_call):
        print(self.base_url, url_to_call)
        returned = requests.get("{}{}".format(self.base_url, url_to_call)).text
        returned = returned.split("itemprop=\"itemListElement\"")

        for element in returned:
            if element.startswith(">") and "</span" in element:
                word = element[:element.find("</span")][1:]
                self.all_words.append(word)

    def generate_jokes(self):
        number_list = []
        stary_procent = 0
        for key, value in self.words_dict.items():
            number_list.append(key)
        number_list.sort(reverse=True)
        for number in number_list:
            min_index = number-1
            if (min_index) not in number_list:
                break
            for word in self.words_dict.get(number):
                self.liczba_slow+=1
                if word[1:] in self.words_dict.get(min_index):
                    # procent = self.words_dict.get(number).index(word) / len(self.words_dict.get(number)) * 100
                    procent = self.liczba_slow / self.liczba_wszystkich_slow * 100
                    if procent != stary_procent:
                        print("Wykonano {:f} %".format(stary_procent))
                        stary_procent = procent
                    self.save_jokes(self.__generate_joke(word, word[1:]))
                    continue

    def __generate_joke(self, first_word, second_word):
        return "Jak jest {} bez {} ?\n{}!\n".format(first_word, second_word, first_word[0])

    def save_jokes(self, joke):
        with open("joke.txt", 'a') as file:
            file.write(joke)

    def add_words_to_database(self):
        db = SessionLocal()
        Base.metadata.create_all(bind=engine)
        for word in self.all_words:
            new_word = WordModel(word, len(word))
            db.add(new_word)
            db.commit()
        db.close()

    # def merge_find(self, szukane, lista, dlugosc):


if __name__ == "__main__":
    mjfpl = MagicJokeFromPolishLanguage()
    url_list = mjfpl.get_all_hrefs_from_page()
    url_sub_list = mjfpl.get_all_subhrefs_from_page(url_list)
    for element in url_sub_list:
        mjfpl.get_words(element)
        print("Zbieranie slow, zebrano juz: {}".format(len(mjfpl.all_words)))
    print("Koniec zbierania slow. Zebrano {}".format(len(mjfpl.all_words)))
    mjfpl.clean_up_word()
    print("Koniec czyszczenia slownika")
    mjfpl.generate_jokes()
    print("Wygenerowalo zarty, czas na zapis")
    mjfpl.save_jokes()