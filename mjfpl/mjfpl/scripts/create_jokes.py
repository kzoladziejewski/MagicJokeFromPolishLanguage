from mjfpl.model.jokes_model import JokeModel
from mjfpl.model.words_model import WordsModel

words = WordsModel.find_all_word()

for word in words:
    noun = word.json().get("nouns")
    if len(noun) > 1:
        for element in range(1, len(noun)):
            gen_first = WordsModel.find_genitive(noun[element:])
            if gen_first:
                gen = gen_first.json().get("genitive")
                joke = f"Jak jest {noun} bez {gen}"
                find_joke = JokeModel.find_skip_repeated_joke(joke)
                if not find_joke:
                    jok = JokeModel(joke_question=joke, joke_answer=noun[:1])
                    jok.save_to_db()