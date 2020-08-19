import requests

class MagicJokeFromPolishLanguage:

    def __init__(self):
        self.base_url = "https://polski-slownik.pl/"
        self.base_page = "https://polski-slownik.pl/wszystkie-slowa-jezyka-polskiego.php"
        self.all_words = []
        self.jokes = []

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
        for first_word in self.all_words:
            for second_word in self.all_words:
                if self.compare_string(first_word, second_word):
                    self.jokes.append(self.__generate_joke(first_word, second_word))

    def __generate_joke(self, first_word, second_word):
        return "Jak jest {} bez {} ? \n {} \n\n!".format(first_word, second_word, first_word[0])

    def save_jokes(self):
        with open("joke.txt") as file:
            file.write(self.jokes)

if __name__ == "__main__":
    mjfpl = MagicJokeFromPolishLanguage()
    url_list = mjfpl.get_all_hrefs_from_page()
    url_sub_list = mjfpl.get_all_subhrefs_from_page(url_list)
    for element in url_sub_list:
        mjfpl.get_words(element)
        print("Zbieranie slow, zebrano juz: {}".format(len(mjfpl.all_words)))
    print("Koniec zbierania slow. Zebrano {}".format(len(mjfpl.all_words)))
    mjfpl.generate_jokes()
    mjfpl.save_jokes()