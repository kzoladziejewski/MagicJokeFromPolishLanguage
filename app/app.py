import requests

from collections import defaultdict
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
                if self.merge_find(word[1:], self.words_dict.get(min_index), len(self.words_dict.get(min_index))):
                    procent = int(self.liczba_slow / self.liczba_wszystkich_slow * 100)
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

    def clean_up_word(self):
        for word in self.all_words:
            word = word.replace("ą","a").replace("ć","c").replace("ę","e").replace("ł","l").replace("ń","n").replace("ó",'o').replace("ż",'z').replace("ś","s").replace("ź","z")
            self.words_dict[len(word)].append(word)
        for val in self.words_dict.keys():
            self.liczba_wszystkich_slow+=len(self.words_dict.get(val))

    def merge_find(self, looking, lista_words, index):
        new_list = []
        new_index = int(index/2)
        print(lista_words)
        print(index)
        if index == 0:
            if looking == lista_words[index]:
                return True
            return False
        # if looking == lista_words[index]:
        #     return True
        if looking < lista_words[new_index]:
            print(lista_words[new_index])
            print("odpalilem sie")
            new_list = lista_words[:new_index]
            return self.merge_find(looking, new_list, new_index)
        elif looking >= lista_words[new_index]:
            new_list = lista_words[new_index:]
            return self.merge_find(looking, new_list, new_index)


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