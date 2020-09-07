class MagicJokeFromPolishLanguage:

    def __init__(self):
        self.base_url = "https://polski-slownik.pl/"
        self.base_page = "https://polski-slownik.pl/wszystkie-slowa-jezyka-polskiego.php"
        self.all_words = []
        self.jokes = []
        self.words_dict = {}
        self.liczba_slow = 0
        self.liczba_wszystkich_slow = 0

    def read_txt_with_words(self):
        with open("odm.txt", 'r', encoding="utf-8") as file:
            all_words = file.read().replace(", ","\n").split("\n")
            for word in all_words:
                try:
                    new_word = word.replace(" ","")
                    self.all_words.append(new_word)
                    self.liczba_wszystkich_slow += 1
                except UnicodeEncodeError:
                    continue

    def generate_jokes(self):
        stary_procent = 0
        lista_numerow = []
        for number in self.words_dict.keys():
            lista_numerow.append(number)
        lista_numerow.sort(reverse=True)
        minimalny_index = lista_numerow[-1]

        for numer in lista_numerow:
            if numer == minimalny_index:
                break
            for lista_slow in self.words_dict.get(numer).values():
                for word in lista_slow:
                    self.liczba_slow +=1
                    procent = int(self.liczba_slow / self.liczba_wszystkich_slow * 100)
                    if procent != stary_procent:
                        print("Wykonano {:f} %".format(stary_procent))
                        stary_procent = procent
                    slownik_danego_numeru = self.words_dict.get(numer-1, None)
                    if slownik_danego_numeru:
                        if slownik_danego_numeru.get(word[1], None):
                            if self.merge_find(word, slownik_danego_numeru.get(word[1])):
                                self.save_jokes(self.__generate_joke(word, word[0:]))

    def __generate_joke(self, first_word, second_word):
        return "Jak jest {} bez {} ?\n{}!\n".format(first_word, second_word, first_word[0])

    def save_jokes(self, joke):
        with open("joke_merge.txt", 'a') as file:
            file.write(joke)

    def clean_up_word(self):
        index_list = set()
        for word_1 in self.all_words:
            word = word_1.lower()
            if len(word) == 0:
                continue
            if not self.words_dict.get(len(word), None):
                self.words_dict[len(word)] = {word[0]: [word]}

            elif not self.words_dict.get(len(word)).get(word[0], None):
                self.words_dict[len(word)].update({word[0]: [word]})
            elif self.words_dict.get(len(word)).get(word[0]):
                self.words_dict[len(word)][word[0]].append(word)
            index_list.add(len(word))
        for val in self.words_dict.keys():
            self.liczba_wszystkich_slow+=len(self.words_dict.get(val))
        for element in index_list:
            for key in self.words_dict[element]:
                self.words_dict[element][key].sort()

    def merge_find(self, looking, lista_words):

        if lista_words:
            index = len(lista_words)
            new_index = int(index / 2)
            if index % 2 == 1:
               new_index = int(index/2) +1
            if len(lista_words) == 1:
                if looking[1:] in lista_words:
                    return True
                return False
            if looking < lista_words[new_index]:
                new_list = lista_words[:new_index]
                return self.merge_find(looking, new_list)
            elif looking >= lista_words[new_index]:
                new_list = lista_words[new_index:]
                return self.merge_find(looking, new_list)


if __name__ == "__main__":
    mjfpl = MagicJokeFromPolishLanguage()
    mjfpl.read_txt_with_words()

    print("Koniec zbierania slow. Zebrano {}".format(len(mjfpl.all_words)))
    mjfpl.clean_up_word()
    print("Koniec czyszczenia slownika")
    mjfpl.all_words = []
    mjfpl.generate_jokes()
    print("Wygenerowalo zarty, czas na zapis")
