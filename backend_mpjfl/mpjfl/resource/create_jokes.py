from flask_restful import Resource

from mpjfl.model.jokes_model import JokeModel
from mpjfl.model.words_model import WordsModel
class CreateJokeResource(Resource):

    def get(self):
        words = WordsModel.find_all_word()
        # core = f"Jak jest {} bez {}"

        for word in words:
            noun = word.json().get("nouns")
            if len(noun) > 1:
                gen_first = WordsModel.find_genitive(noun[1:])

                if gen_first:
                    gen = gen_first.json().get("genitive")
                    joke =  f"Jak jest {noun} bez {gen}"
                    find_joke = JokeModel.find_skip_repeated_joke(joke)
                    if not find_joke:
                        jok = JokeModel(joke_question = joke, joke_answer=noun[:1])
                        jok.save_to_db()
