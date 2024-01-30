from flask_restful import Resource

try:
    from model.jokes_model import JokeModel
    from model.words_model import WordsModel
except ModuleNotFoundError:
    from mjfpl.src.model.jokes_model import JokeModel
    from mjfpl.src.model.words_model import WordsModel

from http import HTTPStatus


class CreateJokeResource(Resource):

    def get(self):
        words = WordsModel.find_all_word()

        for word in words:
            noun = word.json().get("nouns")
            if len(noun) > 1:
                gen_first = WordsModel.find_genitive(noun[1:])

                if gen_first:
                    gen = gen_first.json().get("genitive")
                    joke = f"Jak jest {noun} bez {gen}"
                    find_joke = JokeModel.find_skip_repeated_joke(joke)
                    if not find_joke:
                        jok = JokeModel(joke_question=joke, joke_answer=noun[:1])
                        jok.save_to_db()
        return {HTTPStatus.OK, {"msg": {"Jokes created"}}}
